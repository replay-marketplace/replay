# TT-Metal Python Host APIs

This document provides a comprehensive reference for the Python bindings of TT-Metal host APIs, which allow you to create and manage programs, kernels, buffers, and other resources on Tenstorrent hardware.

## Table of Contents

- [Program Management](#program-management)
- [Kernel Creation](#kernel-creation)
- [Buffer Management](#buffer-management)
- [Circular Buffers](#circular-buffers)
- [Semaphores](#semaphores)
- [Runtime Arguments](#runtime-arguments)
- [Program Descriptors](#program-descriptors)

## Program Management

### CreateProgram

```python
program = ttnn.CreateProgram()
```

Creates a Program object which is the main container that bundles kernels, circular buffers, and/or semaphores for execution on device.

**Returns:** Program object

**Example:**
```python
import ttnn

# Create a new program
program = ttnn.CreateProgram()
```

## Kernel Creation

### CreateKernel

```python
kernel_id = ttnn.CreateKernel(
    program,
    file_name,
    core_spec,
    config=None
)
```

Creates a data movement kernel from a file and adds it to the program.

**Parameters:**
- `program` (Program): The program to which this kernel will be added
- `file_name` (str): Path to kernel source file. Can be absolute/relative to CWD, or relative to TT_METAL_HOME/TT_METAL_KERNEL_PATH
- `core_spec` (CoreCoord | CoreRange | CoreRangeSet): Cores where kernel is placed
- `config` (DataMovementConfig | ComputeConfig | EthernetConfig, optional): Kernel configuration

**Returns:** Kernel ID (int)

**Example:**
```python
# Create a compute kernel on a single core
kernel_id = ttnn.CreateKernel(
    program,
    "kernels/compute.cpp",
    ttnn.CoreCoord(0, 0),
    ttnn.ComputeConfig(
        math_fidelity=ttnn.MathFidelity.HiFi4,
        fp32_dest_acc_en=True
    )
)

# Create a kernel on a range of cores
kernel_id = ttnn.CreateKernel(
    program,
    "kernels/dataflow.cpp",
    ttnn.CoreRange(
        ttnn.CoreCoord(0, 0),
        ttnn.CoreCoord(3, 3)
    )
)
```

### CreateKernelFromString

```python
kernel_id = ttnn.CreateKernelFromString(
    program,
    kernel_src_code,
    core_spec,
    config=None
)
```

Creates a kernel from inline source code string and adds it to the program.

**Parameters:**
- `program` (Program): The program to which this kernel will be added
- `kernel_src_code` (str): Source code for kernel
- `core_spec` (CoreCoord | CoreRange | CoreRangeSet): Cores where kernel is placed
- `config` (DataMovementConfig | ComputeConfig | EthernetConfig, optional): Kernel configuration

**Returns:** Kernel ID (int)

**Example:**
```python
kernel_source = """
#include <stdint.h>
#include "dataflow_api.h"

void kernel_main() {
    uint32_t src_addr = get_arg_val<uint32_t>(0);
    uint32_t dst_addr = get_arg_val<uint32_t>(1);
    // Kernel implementation
}
"""

kernel_id = ttnn.CreateKernelFromString(
    program,
    kernel_source,
    ttnn.CoreCoord(0, 0),
    ttnn.DataMovementConfig()
)
```

## Buffer Management

### CreateBuffer

```python
# Interleaved buffer
buffer = ttnn.CreateBuffer(
    ttnn.InterleavedBufferConfig(
        device=device,
        size=buffer_size,
        page_size=page_size,
        buffer_type=ttnn.BufferType.DRAM
    )
)

# Sharded buffer
buffer = ttnn.CreateBuffer(
    ttnn.ShardedBufferConfig(
        device=device,
        size=buffer_size,
        page_size=page_size,
        buffer_type=ttnn.BufferType.L1,
        shard_parameters=shard_params
    )
)

# With specific address
buffer = ttnn.CreateBuffer(
    config,
    address=0x1000
)

# With sub-device ID
buffer = ttnn.CreateBuffer(
    config,
    sub_device_id=0
)
```

Creates a pre-allocated buffer on device.

**Parameters:**
- `config` (InterleavedBufferConfig | ShardedBufferConfig): Buffer configuration
- `address` (int, optional): Device address of the buffer
- `sub_device_id` (int, optional): Sub-device ID to allocate on

**Returns:** Buffer object

**Example:**
```python
# Create a DRAM buffer
dram_buffer = ttnn.CreateBuffer(
    ttnn.InterleavedBufferConfig(
        device=device,
        size=1024 * 1024,  # 1MB
        page_size=1024,
        buffer_type=ttnn.BufferType.DRAM
    )
)

# Create an L1 buffer
l1_buffer = ttnn.CreateBuffer(
    ttnn.InterleavedBufferConfig(
        device=device,
        size=32 * 1024,  # 32KB
        page_size=1024,
        buffer_type=ttnn.BufferType.L1
    )
)
```

### DeallocateBuffer

```python
ttnn.DeallocateBuffer(buffer)
```

Deallocates buffer from device by marking its memory as free.

**Parameters:**
- `buffer` (Buffer): The buffer to deallocate

**Example:**
```python
# Deallocate a buffer when done
ttnn.DeallocateBuffer(my_buffer)
```

### AssignGlobalBufferToProgram

```python
ttnn.AssignGlobalBufferToProgram(buffer, program)
```

Gives the specified program ownership of the buffer. The buffer will remain on device at least until the program is enqueued. Required for asynchronous Command Queues.

**Parameters:**
- `buffer` (Buffer): The buffer that will be owned by the program
- `program` (Program): The program getting ownership of the buffer

**Example:**
```python
# Assign buffer to program for async execution
ttnn.AssignGlobalBufferToProgram(input_buffer, program)
ttnn.AssignGlobalBufferToProgram(output_buffer, program)
```

## Circular Buffers

### CreateCircularBuffer

```python
cb_id = ttnn.CreateCircularBuffer(
    program,
    core_spec,
    config
)
```

Creates a Circular Buffer (CB) in L1 memory and adds it to the program. Maximum of 32 circular buffers per core.

**Parameters:**
- `program` (Program): The program to which buffer will be added
- `core_spec` (CoreCoord | CoreRange | CoreRangeSet): Cores where CB will be configured
- `config` (CircularBufferConfig): Configuration for circular buffer

**Returns:** Circular Buffer ID (int)

**Example:**
```python
# Create a circular buffer for intermediate data
cb_config = ttnn.CircularBufferConfig(
    total_size=32 * 1024,  # 32KB
    page_size=2048,
    data_format=ttnn.DataFormat.Float16_b,
    buffer_type=ttnn.BufferType.L1
)

cb_id = ttnn.CreateCircularBuffer(
    program,
    ttnn.CoreRange(
        ttnn.CoreCoord(0, 0),
        ttnn.CoreCoord(1, 1)
    ),
    cb_config
)
```

### GetCircularBufferConfig

```python
config = ttnn.GetCircularBufferConfig(program, cb_handle)
```

Gets the configuration of a circular buffer.

**Parameters:**
- `program` (Program): The program containing the circular buffer
- `cb_handle` (int): ID of the circular buffer

**Returns:** CircularBufferConfig

### UpdateCircularBufferTotalSize

```python
ttnn.UpdateCircularBufferTotalSize(program, cb_handle, total_size)
```

Update the total size of a circular buffer.

**Parameters:**
- `program` (Program): The program containing the circular buffer
- `cb_handle` (int): ID of the circular buffer
- `total_size` (int): New size in bytes

### UpdateCircularBufferPageSize

```python
ttnn.UpdateCircularBufferPageSize(
    program,
    cb_handle,
    buffer_index,
    page_size
)
```

Update the page size at specified buffer index.

**Parameters:**
- `program` (Program): The program containing the circular buffer
- `cb_handle` (int): ID of the circular buffer
- `buffer_index` (int): Buffer index (0 to NUM_CIRCULAR_BUFFERS - 1)
- `page_size` (int): Updated page size in bytes

### UpdateDynamicCircularBufferAddress

```python
ttnn.UpdateDynamicCircularBufferAddress(program, cb_handle, buffer)
```

Update the address of a dynamic circular buffer.

**Parameters:**
- `program` (Program): The program containing the circular buffer
- `cb_handle` (int): ID of the circular buffer
- `buffer` (Buffer): L1 buffer that shares address space with CB

## Semaphores

### CreateSemaphore

```python
semaphore_id = ttnn.CreateSemaphore(
    program,
    core_spec,
    initial_value,
    core_type=ttnn.CoreType.WORKER
)
```

Initializes semaphore on cores within core range. Each core can have up to 8 semaphores.

**Parameters:**
- `program` (Program): The program to which semaphore will be added
- `core_spec` (CoreRange | CoreRangeSet): Range of cores using the semaphore
- `initial_value` (int): Initial value of the semaphore
- `core_type` (CoreType, optional): Tensix or Ethernet core type

**Returns:** Semaphore ID (int)

**Example:**
```python
# Create a semaphore for synchronization
sem_id = ttnn.CreateSemaphore(
    program,
    ttnn.CoreRange(
        ttnn.CoreCoord(0, 0),
        ttnn.CoreCoord(3, 3)
    ),
    initial_value=0
)
```

## Runtime Arguments

### SetRuntimeArgs

```python
# Set args for single core or core range
ttnn.SetRuntimeArgs(
    program,
    kernel_id,
    core_spec,
    runtime_args
)

# Set different args for multiple cores
ttnn.SetRuntimeArgs(
    program,
    kernel_id,
    core_coords,  # List of CoreCoord
    runtime_args  # List of lists
)

# Async mode with command queue
ttnn.SetRuntimeArgs(
    device,
    kernel,
    core_spec,
    runtime_args
)
```

Set runtime arguments for a kernel. Maximum 255 runtime args per core.

**Parameters:**
- `program` (Program) or `device` (Device): Program or device for async mode
- `kernel_id` (int) or `kernel` (Kernel): Kernel ID or kernel object
- `core_spec`: Core specification (varies by overload)
- `runtime_args`: Runtime arguments to set

**Example:**
```python
# Set runtime args for a single core
ttnn.SetRuntimeArgs(
    program,
    kernel_id,
    ttnn.CoreCoord(0, 0),
    [src_buffer.address(), dst_buffer.address(), data_size]
)

# Set different args for multiple cores
core_coords = [ttnn.CoreCoord(0, i) for i in range(4)]
runtime_args = [
    [src_buffer.address(), dst_buffer.address() + i * 1024, 1024]
    for i in range(4)
]
ttnn.SetRuntimeArgs(program, kernel_id, core_coords, runtime_args)
```

### GetRuntimeArgs

```python
# Get args for single core
args = ttnn.GetRuntimeArgs(program, kernel_id, logical_core)

# Get args for all cores
all_args = ttnn.GetRuntimeArgs(program, kernel_id)
```

Get runtime arguments for a kernel.

**Parameters:**
- `program` (Program): The program containing the kernel
- `kernel_id` (int): ID of the kernel
- `logical_core` (CoreCoord, optional): Specific core to get args for

**Returns:** Runtime arguments

### SetCommonRuntimeArgs

```python
ttnn.SetCommonRuntimeArgs(program, kernel_id, runtime_args)
```

Set common runtime arguments shared by all cores.

**Parameters:**
- `program` (Program): The program containing the kernel
- `kernel_id` (int): ID of the kernel
- `runtime_args` (list): Common runtime arguments

### GetCommonRuntimeArgs

```python
args = ttnn.GetCommonRuntimeArgs(program, kernel_id)
```

Get common runtime arguments for a kernel.

**Parameters:**
- `program` (Program): The program containing the kernel
- `kernel_id` (int): ID of the kernel

**Returns:** Common runtime arguments

## Program Descriptors

Program descriptors provide a declarative way to define programs with all their components.

### CBFormatDescriptor

```python
format_desc = ttnn.CBFormatDescriptor(
    buffer_index=0,
    data_format=ttnn.DataType.BFLOAT16,  # or ttnn.DataFormat.Float16_b
    page_size=2048
)
```

Descriptor for command buffer format configuration.

### CBDescriptor

```python
cb_desc = ttnn.CBDescriptor(
    total_size=32 * 1024,
    core_ranges=ttnn.CoreRangeSet([
        ttnn.CoreRange(
            ttnn.CoreCoord(0, 0),
            ttnn.CoreCoord(1, 1)
        )
    ]),
    format_descriptors=[format_desc]
)
```

Command buffer descriptor with size, cores, and format.

### ComputeConfigDescriptor

```python
compute_config = ttnn.ComputeConfigDescriptor()
compute_config.math_fidelity = ttnn.MathFidelity.HiFi4
compute_config.fp32_dest_acc_en = True
compute_config.dst_full_sync_en = False
compute_config.unpack_to_dest_mode = [ttnn.UnpackToDestMode.Default]
compute_config.bfp8_pack_precise = True
compute_config.math_approx_mode = False
```

Configuration for compute operations.

### KernelDescriptor

```python
kernel_desc = ttnn.KernelDescriptor(
    kernel_source="kernels/compute.cpp",
    source_type=ttnn.SourceType.FILE_PATH,  # or INLINE
    core_ranges=ttnn.CoreRangeSet([core_range]),
    compile_time_args={"BLOCK_SIZE": 32},
    defines={"ENABLE_OPTIMIZATION": "1"},
    runtime_args=[[buffer1.address(), buffer2.address()]],
    common_runtime_args=[shared_value],
    opt_level=ttnn.KernelBuildOptLevel.FAST,
    config=compute_config
)
```

Complete kernel descriptor with source, configuration, and arguments.

### ProgramDescriptor

```python
program_desc = ttnn.ProgramDescriptor(
    kernels=[kernel_desc1, kernel_desc2],
    semaphores=[sem_desc1, sem_desc2],
    cbs=[cb_desc1, cb_desc2]
)
```

Complete program descriptor bundling kernels, semaphores, and circular buffers.