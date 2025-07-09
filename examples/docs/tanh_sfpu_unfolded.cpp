// SPDX-FileCopyrightText: © 2023 Tenstorrent Inc.
//
// SPDX-License-Identifier: Apache-2.0

//#include <cstdint>
//#include "compute_kernel_api/common.h"
#include "compute_kernel_api/tile_move_copy.h"
#include "compute_kernel_api/eltwise_unary/eltwise_unary.h"
#include "llk_math_eltwise_unary_sfpu_params.h"

namespace NAMESPACE {

// Unfolded version of tanh_tile_init<false>()
inline void tanh_tile_init_unfolded() {
    // Set constants for tanh calculation
    // These match the constants set in tanh_init<false>()
    uint imm0 = 0x1DFF;  // 0.90625*x
    uint imm1 = 0x481A;  // 0.09375*x + 0.8125
    uint imm2 = 0xFF00;  // 1
    
    // Use the correct namespace for _sfpu_load_imm16_
    ckernel::sfpu::_sfpu_load_imm16_(0, imm0);
    ckernel::sfpu::_sfpu_load_imm16_(1, imm1);
    ckernel::sfpu::_sfpu_load_imm16_(2, imm2);
}

// Unfolded version of calculate_tanh<false, 8>
inline void _calculate_tanh_unfolded(const int iterations) {
    // This is the unfolded version with the following parameters:
    // APPROXIMATION_MODE = false
    // ITERATIONS = 8
    
    // SFPU microcode
    sfpi::vUInt l0 = sfpi::l_reg[sfpi::LRegs::LReg0];
    sfpi::vUInt l1 = sfpi::l_reg[sfpi::LRegs::LReg1];
    sfpi::vUInt l2 = sfpi::l_reg[sfpi::LRegs::LReg2];

    for (int d = 0; d < iterations; d++) {
        sfpi::vFloat val = sfpi::dst_reg[0];
        val = sfpi::lut(val, l0, l1, l2);
        sfpi::dst_reg[0] = val;

        sfpi::dst_reg++;
    }

    sfpi::l_reg[sfpi::LRegs::LReg0] = l0;
    sfpi::l_reg[sfpi::LRegs::LReg1] = l1;
    sfpi::l_reg[sfpi::LRegs::LReg2] = l2;
}

// Define these functions for compatibility with the SFPU_OP_CHAIN_0 define
inline void tanh_tile_init() {
    tanh_tile_init_unfolded();
}

inline void tanh_tile(uint32_t idst) {
// THIS IFDEF IS EXTREMELY IMPORTANT FOR THE COMPILER!!!!
// USE THIS SYNTAX TO CALL THE FUNCTION!!!!
// DO NOT CALL IT DIRECTLY!!!!
#ifdef TRISC_MATH
    llk_math_eltwise_unary_sfpu_params<false>(
        _calculate_tanh_unfolded,
        idst,
        (int)VectorMode::RC,
        8);
#endif
}

void MAIN {
    uint32_t per_core_block_cnt = get_compile_time_arg_val(0);
    uint32_t per_core_block_dim = get_compile_time_arg_val(1);

    init_sfpu(tt::CBIndex::c_0, tt::CBIndex::c_16);
    tanh_tile_init_unfolded();
    
    for (uint32_t block_index = 0; block_index < per_core_block_cnt; block_index++) {
        cb_reserve_back(tt::CBIndex::c_16, per_core_block_dim);
        for (uint32_t tile_index = 0; tile_index < per_core_block_dim; ++tile_index) {
            tile_regs_acquire();

            // Pop tile after tile, copy to DST and pack
            cb_wait_front(tt::CBIndex::c_0, 1);
            copy_tile(tt::CBIndex::c_0, 0, 0);
        
            // Apply tanh operation
            tanh_tile(0);
            
            tile_regs_commit();
            tile_regs_wait();
            pack_tile(0, tt::CBIndex::c_16);

            cb_pop_front(tt::CBIndex::c_0, 1);
            tile_regs_release();
        }
        cb_push_back(tt::CBIndex::c_16, per_core_block_dim);
    }
}
}  // namespace NAMESPACE 