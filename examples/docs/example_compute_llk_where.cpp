// SPDX-FileCopyrightText: © 2025 Tenstorrent Inc.
//
// SPDX-License-Identifier: Apache-2.0

#include "elemwise_where_kernel_args.hpp"
#include "ttnn/kernel/kernel_utils.hpp"

#include "compute_kernel_api.h"
#include "compute_kernel_api/cb_api.h"
#include "compute_kernel_api/tile_move_copy.h"

#include "compute_kernel_api/eltwise_unary/eltwise_unary.h"
#include "compute_kernel_api/eltwise_unary/binop_with_scalar.h"
#include "compute_kernel_api/eltwise_binary.h"

// =============================================================================
// CIRCULAR BUFFER (CB) DEFINITIONS
// =============================================================================
// Circular buffers are the main mechanism for data flow between kernels.
// Each CB acts as a FIFO queue that can hold multiple tiles of data.

constexpr auto cb_condition = tt::CBIndex::c_0;      // Input: condition tensor (bool/float)
constexpr auto cb_true_values = tt::CBIndex::c_1;    // Input: values when condition is true  
constexpr auto cb_false_values = tt::CBIndex::c_2;   // Input: values when condition is false
constexpr auto cb_true_values_out = tt::CBIndex::c_3; // Intermediate: masked true values
constexpr auto cb_out = tt::CBIndex::c_4;            // Output: final result

namespace NAMESPACE {
void MAIN {
    using namespace ttnn::kernel_utils;
    using namespace ttnn::kernel::eltwise::where_args;
    auto args = make_runtime_struct_from_args<ElemwiseComputeKernelArgs>();

    // =============================================================================
    // INITIALIZATION PHASE
    // =============================================================================
    // Initialize compute units for the operations we'll be using.
    // This is a common pattern - initialize all your compute units upfront.
    
    unary_op_init_common(cb_true_values, cb_out);  // Initialize unary operation pipeline
    copy_tile_to_dst_init_short(cb_true_values);   // Initialize tile copy operations

    // =============================================================================
    // MAIN PROCESSING LOOP
    // =============================================================================
    // Process data in blocks. Each block contains multiple tiles.
    // This blocking pattern is essential for efficient memory usage and performance.
    
    for (uint32_t block_index = 0; block_index < args.per_core_block_cnt; block_index++) {
        
        // =========================================================================
        // STEP 1: GENERATE TRUE VALUE MASK
        // =========================================================================
        // Goal: Create a mask where condition > 0, then multiply with true_values
        
        // Wait for condition data to be available in the circular buffer
        cb_wait_front(cb_condition, args.per_core_block_size);

        // IMPORTANT PATTERN: Always acquire tile registers before using them
        tile_regs_acquire();
        
        // Copy condition tile from CB to destination registers (DST)
        copy_tile_to_dst_init_short(cb_condition);
        copy_tile(cb_condition, 0, 0);  // Copy tile 0 from CB to DST register 0

        // Apply greater-than-zero operation to create a boolean mask
        // This converts condition values to 1.0 where condition > 0, 0.0 elsewhere
        ckernel::gtz_tile_init();  // Initialize greater-than-zero SFPU operation
        ckernel::gtz_tile(0);      // Apply GTZ to tile in register 0

        // Now we need the true_values to multiply with our mask
        cb_wait_front(cb_true_values, args.per_core_block_size);

        // BINARY OPERATION PATTERN: Use dest-reuse when one operand is already in DST
        // The mask (result of GTZ) is in DST, true_values comes from CB
        binary_dest_reuse_tiles_init<EltwiseBinaryType::ELWMUL, EltwiseBinaryReuseDestType::DEST_TO_SRCA>(
            cb_true_values);
        binary_dest_reuse_tiles<EltwiseBinaryType::ELWMUL, EltwiseBinaryReuseDestType::DEST_TO_SRCA>(
            cb_true_values, 0, 0);  // Multiply: DST[0] = DST[0] * cb_true_values[0]

        // IMPORTANT PATTERN: Always commit and wait after compute operations
        tile_regs_commit();  // Commit the computation
        tile_regs_wait();    // Wait for it to complete

        // Store the masked true values to intermediate buffer
        cb_reserve_back(cb_true_values_out, args.per_core_block_size);
        pack_tile(0, cb_true_values_out);  // Write DST[0] to cb_true_values_out
        tile_regs_release();  // Release registers for next use
        cb_push_back(cb_true_values_out, args.per_core_block_size);

        // =========================================================================
        // STEP 2: GENERATE FALSE VALUE MASK AND COMBINE
        // =========================================================================
        // Goal: Create mask where condition <= 0, multiply with false_values,
        //       then add to the masked true_values to get final result
        
        cb_wait_front(cb_false_values, args.per_core_block_size);
        cb_wait_front(cb_true_values_out, args.per_core_block_size);  // Need this for final add
        
        tile_regs_acquire();
        
        // Reload the condition into DST (we need it again for the inverse mask)
        copy_tile_to_dst_init_short(cb_condition);
        copy_tile(cb_condition, 0, 0);

        // Apply less-than-or-equal-to-zero to create inverse mask
        // This gives us 1.0 where condition <= 0, 0.0 elsewhere
        ckernel::lez_tile_init();  // Initialize less-than-or-equal-zero SFPU operation  
        ckernel::lez_tile(0);      // Apply LEZ to tile in register 0

        // Multiply inverse mask with false_values
        binary_dest_reuse_tiles_init<EltwiseBinaryType::ELWMUL, EltwiseBinaryReuseDestType::DEST_TO_SRCA>(
            cb_false_values);
        binary_dest_reuse_tiles<EltwiseBinaryType::ELWMUL, EltwiseBinaryReuseDestType::DEST_TO_SRCA>(
            cb_false_values, 0, 0);  // DST[0] = DST[0] * cb_false_values[0]

        // Prepare output buffer
        cb_reserve_back(cb_out, args.per_core_block_size);
        
        // FINAL COMBINATION: Add masked_true_values + masked_false_values
        // Since masks are complementary (one is 0 where other is 1), 
        // this gives us the final where() result
        binary_dest_reuse_tiles_init<EltwiseBinaryType::ELWADD, EltwiseBinaryReuseDestType::DEST_TO_SRCA>(
            cb_true_values_out);
        binary_dest_reuse_tiles<EltwiseBinaryType::ELWADD, EltwiseBinaryReuseDestType::DEST_TO_SRCA>(
            cb_true_values_out, 0, 0);  // DST[0] = DST[0] + cb_true_values_out[0]

        tile_regs_commit();
        tile_regs_wait();
        pack_tile(0, cb_out);  // Write final result to output buffer
        tile_regs_release();

        // =========================================================================
        // CLEANUP PHASE
        // =========================================================================
        // IMPORTANT PATTERN: Always pop data from CBs after processing
        // This frees up space for the next iteration and maintains proper flow control
        
        cb_pop_front(cb_true_values_out, args.per_core_block_size);  // Clean up intermediate
        cb_pop_front(cb_condition, args.per_core_block_size);        // Clean up inputs
        cb_pop_front(cb_true_values, args.per_core_block_size);
        cb_pop_front(cb_false_values, args.per_core_block_size);

        // Make output available to next kernel in the pipeline
        cb_push_back(cb_out, args.per_core_block_size);
    }
}

}  // namespace NAMESPACE

// =============================================================================
// KEY PATTERNS:
// =============================================================================
// 
// 1. RESOURCE MANAGEMENT:
//    - Always acquire tile registers before use: tile_regs_acquire()
//    - Always release after use: tile_regs_release()
//    - Always commit and wait after compute: tile_regs_commit() + tile_regs_wait()
//
// 2. CIRCULAR BUFFER FLOW:
//    - cb_wait_front() before reading data
//    - cb_reserve_back() before writing data  
//    - cb_pop_front() after consuming data
//    - cb_push_back() after producing data
//
// 3. INITIALIZATION PATTERN:
//    - Initialize all compute units at the beginning
//    - Use _init() functions before first use of each operation type
//
// 4. BINARY OPERATIONS:
//    - Use dest-reuse patterns when one operand is already in DST registers
//    - DEST_TO_SRCA means DST becomes first operand, CB becomes second
//
// 5. TILE FLOW:
//    - Data flows: CB -> DST registers -> Compute -> DST registers -> CB
//    - Use copy_tile() to move data from CB to DST
//    - Use pack_tile() to move data from DST to CB
//
// 6. OPERATION COMPOSITION:
//    - Complex operations are built by chaining simple primitives
//    - Use intermediate CBs to store partial results
//    - This where() operation combines: copy + SFPU + binary ops