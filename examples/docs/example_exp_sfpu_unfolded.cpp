/**
 * TENSTORRENT LOW LEVEL KERNEL: EXPONENTIAL FUNCTION
 * 
 * This kernel implements the exponential (e^x) function on Tenstorrent's AI accelerator hardware.
 * It processes data in "tiles" (typically 32x32 elements) using the Special Function Processing Unit (SFPU).
 * 
 * KEY CONCEPTS FOR JUNIOR ENGINEERS:
 * - Tiles: Basic data unit (32x32 fp16/fp32 elements) that flows through the compute pipeline
 * - SFPU: Special Function Processing Unit for complex math (exp, log, sigmoid, etc.)
 * - Circular Buffers (CB): Hardware-managed memory buffers for data movement between cores
 * - DEST Registers: Intermediate storage where SFPU operations are performed
 * - Unfolding: Manual optimization technique replacing function calls with inline code
 */

#include "compute_kernel_api/tile_move_copy.h"
#include "compute_kernel_api/eltwise_unary/eltwise_unary.h"
#include "llk_math_eltwise_unary_sfpu_params.h"

namespace NAMESPACE {

//=============================================================================
// EXPONENTIAL INITIALIZATION
//=============================================================================

/**
 * Initialize SFPU constants for exponential calculation
 * 
 * MATHEMATICAL BACKGROUND:
 * The exponential function e^x is computed using range reduction and polynomial
 * approximation. We first reduce the input to a manageable range, then use a
 * polynomial series to approximate the result.
 * 
 * CONSTANTS EXPLAINED:
 * - 1.442695f: 1/ln(2), used for converting from base-e to base-2
 * - 2.0f: Used in the polynomial evaluation
 * - 0.863281f: Coefficient from the polynomial approximation series
 */
inline void exp_tile_init_unfolded() {
    // The SFPU has 4 programmable FP32 constant registers that can be accessed
    // during mathematical operations
    sfpi::vConstFloatPrgm0 = 1.442695f;  // ln2_recip = 1/ln(2) for base conversion
    sfpi::vConstFloatPrgm1 = 2.0f;
    sfpi::vConstFloatPrgm2 = 0.863281f;  // Polynomial coefficient for approximation
}

//=============================================================================
// CORE EXPONENTIAL ALGORITHM
//=============================================================================

/**
 * Compute exponential function for a vector of values using SFPU
 */
sfpi_inline sfpi::vFloat _sfpu_exp_(sfpi::vFloat val) {
    // RANGE REDUCTION: Extract exponent and handle large values to prevent overflow
    sfpi::vInt exp = exexp(val);
    
    v_if (exp >= 0) {
        val = setexp(val, 126);  // Replace exponent with -1 (126 in biased representation)
    }
    v_endif;

    // POLYNOMIAL APPROXIMATION using Horner's method for efficiency
    sfpi::vFloat tmp = val * sfpi::vConst0p8373 + sfpi::s2vFloat16b(0.863281);
    val = val * tmp + sfpi::vConst1;

    // RESULT RECONSTRUCTION: Scale back up using repeated squaring
    v_if (exp >= 0) {
        val = val * val;
        
        // Up to 7 iterations for IEEE float range
        for (int s_iter = 0; s_iter < 7; s_iter++) {
            exp = exp - 1;
            v_and(exp >= 0);  // Narrow predication
            val = val * val;
        }
    }
    v_endif;

    return val;
}

//=============================================================================
// TILE-LEVEL EXPONENTIAL PROCESSING
//=============================================================================

/**
 * Process a complete tile through the exponential function
 * 
 * ITERATION COUNT:
 * - iterations = 8: This processes 8 "rows" worth of data at a time
 * - Each SFPU instance handles 4 rows simultaneously
 * - Total of 32 rows processed (8 iterations × 4 rows per iteration)
 * 
 * MATHEMATICAL INSIGHT: 
 * For negative inputs, we use the identity e^(-x) = 1/e^x
 * This avoids numerical issues with the polynomial approximation
 */
inline void _calculate_exponential_unfolded(const int iterations) {
    for (int d = 0; d < iterations; d++) {
        sfpi::vFloat val = sfpi::dst_reg[0];
        
        // Compute e^|x| (exponential of absolute value)
        sfpi::vFloat result = _sfpu_exp_(sfpi::setsgn(val, 0));

        // Handle negative inputs: if input was negative, take reciprocal
        v_if (val < 0) {
            result = ckernel::sfpu::_sfpu_reciprocal_(result);
        }
        v_endif;

        sfpi::dst_reg[0] = result;
        sfpi::dst_reg++;
    }
}

/**
 * Execute exponential operation on a tile using SFPU
 * 
 * CRITICAL COMPILER DIRECTIVE:
 * The #ifdef TRISC_MATH guard ensures this code only compiles for the
 * math processing thread. This is essential for the Tenstorrent toolchain.
 */
inline void exp_tile_unfolded(uint32_t idst) {
    // THIS IFDEF IS CRITICAL FOR THE TENSTORRENT COMPILER!
    // Only compile this code when building for the math processing thread
#ifdef TRISC_MATH
    llk_math_eltwise_unary_sfpu_params<false>(
        _calculate_exponential_unfolded,
        idst,
        (int)VectorMode::RC,
        8);
#endif
}

//=============================================================================
// MAIN KERNEL EXECUTION
//=============================================================================

/**
 * Main kernel function - processes blocks of tiles through exponential operation
 * 
 * TENSTORRENT EXECUTION MODEL:
 * 1. Data flows through circular buffers between cores
 * 2. Input data arrives in CB c_0, output goes to CB c_16
 * 3. Processing happens tile-by-tile with proper synchronization
 * 4. Double-buffering ensures continuous data flow
 */
void MAIN {
    uint32_t per_core_block_cnt = get_compile_time_arg_val(0);
    uint32_t per_core_block_dim = get_compile_time_arg_val(1);

    // Set up SFPU to read from input CB (c_0) and write to output CB (c_16)
    init_sfpu(tt::CBIndex::c_0, tt::CBIndex::c_16);
    exp_tile_init_unfolded();

    for (uint32_t block_index = 0; block_index < per_core_block_cnt; block_index++) {
        
        // Reserve space in output circular buffer for this block's results
        cb_reserve_back(tt::CBIndex::c_16, per_core_block_dim);
        
        for (uint32_t tile_index = 0; tile_index < per_core_block_dim; ++tile_index) {
            
            tile_regs_acquire();

            // Wait for input data to be available, then copy to working registers
            cb_wait_front(tt::CBIndex::c_0, 1);
            copy_tile(tt::CBIndex::c_0, 0, 0);
        
            // Apply exponential operation
            exp_tile_unfolded(0);
            
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