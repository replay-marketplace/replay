# TT-Metal Kernel APIs Reference Guide

**PURPOSE**: Comprehensive reference for diagnosing compilation errors and correctness issues in TT-Metal kernels

**REPO_PATH**: `/home/jmalone/work/tt-metal`

---

## CRITICAL PATTERNS FOR LLM ANALYSIS

### KERNEL TYPE IDENTIFICATION
```cpp
// DATA MOVEMENT KERNELS (reader/writer)
#include "dataflow_api.h"
void kernel_main() { /* uses NOC, CB operations */ }

// COMPUTE KERNELS  
#include "compute_kernel_api.h"
namespace NAMESPACE {
void MAIN { /* uses tile operations, SFPU */ }
}
```

### COMMON COMPILATION ERROR PATTERNS
- **Missing namespace**: Compute kernels MUST use `namespace NAMESPACE { void MAIN { } }`
- **Missing headers**: Each operation type needs specific includes
- **CB index mismatch**: Input CBs typically c_0, c_1; Output CBs typically c_16, c_17
- **Uninitialized SFPU**: All SFPU operations need `*_init()` calls
- **Wrong function signatures**: Check parameter counts and types

---

## HEADER FILE MAPPING

### CORE HEADERS
| Header | Purpose | Key Functions |
|--------|---------|---------------|
| `dataflow_api.h` | Data movement | `noc_async_read()`, `cb_wait_front()`, `cb_push_back()` |
| `compute_kernel_api.h` | Main compute | `tile_regs_acquire()`, `copy_tile()`, `pack_tile()` |
| `compute_kernel_api/common.h` | Runtime args | `get_arg_val()`, `get_compile_time_arg_val()` |
| `compute_kernel_api/cb_api.h` | Circular buffers | `cb_wait_front()`, `cb_pop_front()`, `cb_reserve_back()` |
| `compute_kernel_api/tile_move_copy.h` | Tile movement | `copy_tile()`, `copy_tile_init()` |

### SFPU OPERATION HEADERS
| Header | Functions | Common Errors |
|--------|-----------|---------------|
| `eltwise_unary/exp.h` | `exp_tile()`, `exp_tile_init()` | Missing ckernel:: namespace |
| `eltwise_unary/negative.h` | `negative_tile()`, `negative_tile_init()` | Not calling init function |
| `eltwise_binary_sfpu.h` | `add_binary_tile()`, `mul_binary_tile()`, `div_binary_tile()`, `sub_binary_tile()`  | Using wrong add_tiles function |
| `eltwise_unary/binop_with_scalar.h` | `mul_unary_tile()`, `div_unary_tile()` | Wrong scalar format |
| `eltwise_binary.h` | `add_tiles()`, `sub_tiles()` | CB-based, not DST register |

---

## SFPU OPERATIONS REFERENCE

### MATHEMATICAL FUNCTIONS
```cpp
// EXPONENTIAL/LOGARITHMIC
#include "compute_kernel_api/eltwise_unary/exp.h"
ckernel::exp_tile_init();
ckernel::exp_tile(dst_reg_idx);

#include "compute_kernel_api.h"
ckernel::log_tile_init();
ckernel::log_tile(dst_reg_idx);
ckernel::abs_tile_init();
ckernel::abs_tile(dst_reg_idx);
ckernel::sign_tile_init();
ckernel::sign_tile(dst_reg_idx);

// TRIGONOMETRIC
#include "compute_kernel_api/eltwise_unary/trigonometry.h"
ckernel::sin_tile_init();
ckernel::sin_tile(dst_reg_idx);
ckernel::cos_tile(dst_reg_idx);
ckernel::tan_tile(dst_reg_idx);

// OTHER
#include "compute_kernel_api/eltwise_unary/recip.h"
ckernel::recip_init();
ckernel::recip(dst_reg_idx);
```

### ACTIVATION FUNCTIONS
```cpp
// RELU FAMILY
#include "compute_kernel_api/eltwise_unary/relu.h"
ckernel::relu_tile_init();
ckernel::relu_tile(dst_reg_idx);

// GELU
#include "compute_kernel_api/eltwise_unary/gelu.h"
ckernel::gelu_tile_init();
ckernel::gelu_tile(dst_reg_idx);

// SIGMOID
#include "compute_kernel_api/eltwise_unary/sigmoid.h"
ckernel::sigmoid_tile_init();
ckernel::sigmoid_tile(dst_reg_idx);
```

### BINARY OPERATIONS
```cpp
// DST REGISTER OPERATIONS (preferred for efficiency)
#include "compute_kernel_api/eltwise_binary_sfpu.h"
ckernel::add_binary_tile_init();
ckernel::add_binary_tile(dst_reg_0, dst_reg_1);  // Result in dst_reg_0

#include "compute_kernel_api/binary_max_min.h"
ckernel::binary_min_tile_init();
ckernel::binary_min_tile(dst_reg_0, dst_reg_1); // Result in dst_reg_0
ckernel::binary_max_tile_init();
ckernel::binary_max_tile(dst_reg_0, dst_reg_1); // Result in dst_reg_0

// CIRCULAR BUFFER OPERATIONS
#include "compute_kernel_api/eltwise_binary.h"
ckernel::add_tiles_init(cb_in0, cb_in1);
ckernel::add_tiles(cb_in0, cb_in1, tile_idx_0, tile_idx_1, dst_reg_idx);
```

### SCALAR OPERATIONS
```cpp
#include "compute_kernel_api/eltwise_unary/binop_with_scalar.h"
ckernel::binop_with_scalar_tile_init();
ckernel::mul_unary_tile(dst_reg_idx, 0x3F000000);  // Multiply by 0.5
ckernel::div_unary_tile(dst_reg_idx, 0x40000000);  // Divide by 2.0
ckernel::add_unary_tile(dst_reg_idx, 0x40000000);  // Add 2.0
ckernel::sub_unary_tile(dst_reg_idx, 0x40000000);  // Subtract 2.0 from input

// REVERSE SUB
#include "compute_kernel_api/eltwise_unary/reverseops.h"
ckernel::rsub_tile(dst_reg_idx, 0x40000000); // Subtract input from 2.0

// MAX AND MIN
#include "compute_kernel_api.h"
ckernel::unary_min_tile_init();
ckernel::unary_min_tile(dst_reg_idx, 0x3F000000); // Eltwise min of input and 0.5
ckernel::unary_max_tile_init();
ckernel::unary_max_tile(dst_reg_idx, 0x3F000000); // Eltwise max of input and 0.5
```

---

## CIRCULAR BUFFER CONVENTIONS

### STANDARD CB INDICES
```cpp
constexpr auto cb_in0 = tt::CBIndex::c_0;    // Primary input
constexpr auto cb_in1 = tt::CBIndex::c_1;    // Secondary input  
constexpr auto cb_out0 = tt::CBIndex::c_16;  // Primary output
constexpr auto cb_out1 = tt::CBIndex::c_17;  // Secondary output
```

### CB OPERATION PATTERNS
```cpp
// READER PATTERN
cb_reserve_back(cb_out, num_tiles);
// ... fill tiles ...
cb_push_back(cb_out, num_tiles);

// COMPUTE PATTERN  
cb_wait_front(cb_in, num_tiles);
// ... process tiles ...
cb_pop_front(cb_in, num_tiles);

// WRITER PATTERN
cb_wait_front(cb_in, num_tiles);
// ... write tiles ...
cb_pop_front(cb_in, num_tiles);
```

---

## TILE REGISTER MANAGEMENT

### STANDARD TILE OPERATIONS
```cpp
// ACQUIRE/RELEASE PATTERN
tile_regs_acquire();
copy_tile(cb_in, tile_idx, dst_reg_idx);
// ... SFPU operations on dst_reg_idx ...
tile_regs_commit();
tile_regs_wait();
pack_tile(dst_reg_idx, cb_out);
tile_regs_release();
```

### DST REGISTER LIMITS
- **Maximum tiles**: 16 tiles in DST registers simultaneously
- **Typical usage**: 0-7 for compute, 8-15 for intermediate storage
- **Best practice**: Use lowest numbered registers first

---

## COMMON ERROR DIAGNOSIS

### COMPILATION ERRORS
```cpp
// ERROR: 'exp_tile_init' was not declared in this scope
// FIX: Add #include "compute_kernel_api/eltwise_unary/exp.h"

// ERROR: 'MAIN' was not declared in this scope  
// FIX: Add namespace NAMESPACE { void MAIN { } }

// ERROR: 'add_tiles' function parameters don't match
// FIX: Check if you want add_tiles() (CB-based) or add_binary_tile() (DST-based)

// ERROR: 'ckernel' is not a namespace
// FIX: Add ckernel:: prefix to SFPU function calls
```

### RUNTIME ERRORS
```cpp
// ERROR: Incorrect results (values too large/small)
// CHECK: Missing initialization calls (*_init() functions)
// CHECK: Wrong scalar values (IEEE 754 float32 format)
// CHECK: Missing final operations (like division by 2 for cosh)

// ERROR: Segmentation fault
// CHECK: Tile register acquire/release balance
// CHECK: CB size matches tile count
// CHECK: NOC address alignment
```

---

## ARCHITECTURE-SPECIFIC CONSIDERATIONS

### WORMHOLE_B0 vs BLACKHOLE
```cpp
#ifdef ARCH_WORMHOLE_B0
    // Wormhole-specific optimizations
#elif defined(ARCH_BLACKHOLE)
    // Blackhole-specific handling
#endif
```

### PERFORMANCE PATTERNS
- **NOC Optimization**: Use async operations with barriers
- **CB Efficiency**: Match tile counts to CB sizes
- **SFPU Performance**: Call init functions once, not per tile
- **Memory Alignment**: Ensure proper address alignment

---

## DEBUGGING UTILITIES

### DEBUG PRINTING
```cpp
#include "debug/dprint.h"
DPRINT << "Debug message: " << value << ENDL();
DPRINT_MATH(DPRINT << "Math thread message" << ENDL());
DPRINT_DATA0(DPRINT << "Data0 thread message" << ENDL());
```

### ASSERTIONS AND WAYPOINTS
```cpp
#include "debug/assert.h"
#include "debug/waypoint.h"
ASSERT(condition);
WAYPOINT("checkpoint_name");
```

---

## QUICK REFERENCE DECISION TREE

### CHOOSING OPERATION TYPE
```
Need to add two tiles?
├── Tiles in DST registers? → use add_binary_tile()
└── Tiles in CBs? → use add_tiles()

Need exponential function?
├── Add #include "compute_kernel_api/eltwise_unary/exp.h"
├── Call ckernel::exp_tile_init() once
└── Call ckernel::exp_tile(dst_reg_idx) per tile

Getting compilation errors?
├── Missing namespace? → Add namespace NAMESPACE { void MAIN { } }
├── Function not found? → Check header includes
├── Wrong parameters? → Check function signature
└── Namespace issues? → Add ckernel:: prefix
```

---

## FILE LOCATION REFERENCE

### CORE API LOCATIONS
- **Main headers**: `/home/jmalone/work/tt-metal/tt_metal/include/`
- **Compute API**: `/home/jmalone/work/tt-metal/tt_metal/include/compute_kernel_api/`
- **SFPU operations**: `/home/jmalone/work/tt-metal/tt_metal/include/compute_kernel_api/eltwise_unary/`
- **Binary operations**: `/home/jmalone/work/tt-metal/tt_metal/include/compute_kernel_api/eltwise_binary*.h`
- **Data movement**: `/home/jmalone/work/tt-metal/tt_metal/hw/inc/dataflow_api.h`
- **Debug utilities**: `/home/jmalone/work/tt-metal/tt_metal/hw/inc/debug/`

### IMPLEMENTATION LOCATIONS
- **Low-level SFPU**: `/home/jmalone/work/tt-metal/tt_metal/hw/ckernels/[arch]/metal/llk_api/llk_sfpu/`
- **Examples**: `/home/jmalone/work/tt-metal/tt_metal/programming_examples/`
- **Tests**: `/home/jmalone/work/tt-metal/tests/tt_metal/`

---

**END OF REFERENCE GUIDE**
