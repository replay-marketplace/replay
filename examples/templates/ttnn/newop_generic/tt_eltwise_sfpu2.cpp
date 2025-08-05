/**
 * TENSTORRENT LOW LEVEL KERNEL: HYPERBOLIC SINE FUNCTION
 * 
 * This kernel implements the hyperbolic sine (sinh(x)) function on Tenstorrent's AI accelerator hardware.
 * It processes data in "tiles" (typically 32x32 elements) using the Special Function Processing Unit (SFPU).
 * 
 * MATHEMATICAL BACKGROUND:
 * sinh(x) = (e^x - e^(-x)) / 2
 * 
 * IMPLEMENTATION STRATEGY:
 * 1. Copy input x to two DST registers
 * 2. Negate one copy to get -x
 * 3. Compute e^x and e^(-x) using SFPU
 * 4. Subtract e^(-x) from e^x
 * 5. Divide result by 2
 * 
 * KEY CONCEPTS FOR JUNIOR ENGINEERS:
 * - Tiles: Basic data unit (32x32 fp16/fp32 elements) that flows through the compute pipeline
 * - SFPU: Special Function Processing Unit for complex math (exp, log, sigmoid, etc.)
 * - Circular Buffers (CB): Hardware-managed memory buffers for data movement between cores
 * - DEST Registers: Intermediate storage where SFPU operations are performed
 * - Binary Operations: Operations between DST registers for efficient computation
 */

#include "compute_kernel_api.h"
#include "compute_kernel_api/tile_move_copy.h"
#include "compute_kernel_api/eltwise_unary/eltwise_unary.h"
#include "compute_kernel_api/eltwise_unary/exp.h"
#include "compute_kernel_api/eltwise_unary/negative.h"
#include "compute_kernel_api/eltwise_binary.h"
#include "compute_kernel_api/eltwise_binary_sfpu.h"
#include "compute_kernel_api/eltwise_unary/binop_with_scalar.h"
#include "compute_kernel_api/binary_max_min.h"
#include "llk_math_eltwise_unary_sfpu_params.h"

namespace NAMESPACE {

//=============================================================================
// CORE HYPERBOLIC SINE ALGORITHM  
//=============================================================================

/**
 * Compute hyperbolic sine using the identity: sinh(x) = (e^x - e^(-x)) / 2
 * 
 * This function implements the sinh calculation by:
 * 1. Computing e^x and e^(-x) separately  
 * 2. Subtracting to get e^x - e^(-x)
 * 3. Dividing by 2 to get the final result
 * 
 * NOTE: This function works with DST registers rather than SFPU directly,
 * so it uses the higher-level LLK operations for better maintainability.
 */

//=============================================================================
// MAIN KERNEL EXECUTION
//=============================================================================

/**
 * Main kernel function - processes blocks of tiles through hyperbolic sine operation
 * 
 * TENSTORRENT EXECUTION MODEL:
 * 1. Data flows through circular buffers between cores
 * 2. Input data arrives in CB c_0, output goes to CB c_16
 * 3. Processing happens tile-by-tile with proper synchronization
 * 4. Double-buffering ensures continuous data flow
 * 
 * SINH IMPLEMENTATION:
 * Each tile goes through: x -> sinh(x) = (e^x - e^(-x)) / 2
 * This requires multiple DST registers per tile for intermediate computations
 */
void MAIN {
    uint32_t per_core_block_cnt = get_compile_time_arg_val(0);
    uint32_t per_core_block_dim = get_compile_time_arg_val(1);

    // Set up SFPU to read from input CB (c_0) and write to output CB (c_16)
    init_sfpu(tt::CBIndex::c_0, tt::CBIndex::c_16);

    for (uint32_t block_index = 0; block_index < per_core_block_cnt; block_index++) {
        
        // Reserve space in output circular buffer for this block's results
        cb_reserve_back(tt::CBIndex::c_16, per_core_block_dim);
        
        for (uint32_t tile_index = 0; tile_index < per_core_block_dim; ++tile_index) {
            
            tile_regs_acquire();

            // Wait for input data to be available, then copy to working registers
            cb_wait_front(tt::CBIndex::c_0, 1);
            copy_tile(tt::CBIndex::c_0, 0, 0);
            
            // Copy the same input to DST register 1 for -x computation
            copy_tile(tt::CBIndex::c_0, 0, 1);
        
            // Apply hyperbolic sine operation
            // At this point, we have x in both DST[0] and DST[1] from main function
            // DST[0] = x, DST[1] = x
            
            // Initialize negation operation for computing -x
            ckernel::negative_tile_init();
            // Step 1: Negate DST[1] to get -x
            ckernel::negative_tile(1);  // DST[1] = -x
            
            // Initialize exponential SFPU operations for both e^x and e^(-x)
            ckernel::exp_tile_init();
            // Step 2: Compute exponentials
            ckernel::exp_tile(0);  // DST[0] = e^x
            ckernel::exp_tile(1);  // DST[1] = e^(-x)
            
            // Initialize binary subtraction for e^x - e^(-x)  
            ckernel::sub_binary_tile_init();
            // Step 3: Subtract e^(-x) from e^x
            // DST[0] = DST[0] - DST[1] = e^x - e^(-x)
            ckernel::sub_binary_tile(0, 1);
            
            // Initialize scalar division for multiplying by 0.5
            ckernel::binop_with_scalar_tile_init();
            // Step 4: Multiply by 0.5 to get final sinh result (equivalent to dividing by 2)
            // IEEE 754 float32 representation of 0.5 is 0x3F000000
            ckernel::mul_unary_tile(0, 0x3F000000);  // DST[0] = DST[0] * 0.5
            
            tile_regs_commit();
            tile_regs_wait();
            pack_tile(0, tt::CBIndex::c_16);

            cb_pop_front(tt::CBIndex::c_0, 1);
            tile_regs_release();
        }
        
        // Make the completed block available to downstream consumers
        cb_push_back(tt::CBIndex::c_16, per_core_block_dim);
    }
}

} // namespace NAMESPACE
