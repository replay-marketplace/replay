import torch
import pytest
import ttnn
import numpy as np
import os
from loguru import logger

def kernel_path(kernel_file_name):    
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    kernel_dir = current_dir
    return os.path.join(kernel_dir, kernel_file_name)

def prepare_newop_program(device, input_tensor, output_tensor, num_tiles, src_bank_id, dst_bank_id):
    core = ttnn.CoreCoord(0, 0)
    core_grid = ttnn.CoreRangeSet([ttnn.CoreRange(core, core)])

    input_cb_data_format = ttnn.bfloat16  # this will be mapped tt::DataFormat::Float16_b
    cb_total_size = 2 * 2 * 1024  # tt::DataFormat::Float16_b hard coded to have size 2 * 1024
    cb_page_size = 2 * 1024

    in_cb = 0
    out_cb = 16
    in_cb_format = ttnn.CBFormatDescriptor(buffer_index=in_cb, data_format=input_cb_data_format, page_size=cb_page_size,)
    out_cb_format = ttnn.CBFormatDescriptor(buffer_index=out_cb, data_format=input_cb_data_format, page_size=cb_page_size,)
    in_cb_descriptor = ttnn.CBDescriptor(total_size=cb_total_size,core_ranges=core_grid,format_descriptors=[in_cb_format],)
    out_cb_descriptor = ttnn.CBDescriptor(total_size=cb_total_size,core_ranges=core_grid,format_descriptors=[out_cb_format],)

    is_dram_input = 1
    reader_compile_time_args = [is_dram_input]
    writer_compile_time_args = [out_cb, is_dram_input]
    compute_compile_time_args = [num_tiles, 1]
    reader_rt_args = [input_tensor.buffer_address(), num_tiles, 0]
    writer_rt_args = [output_tensor.buffer_address(), num_tiles, 0]


    # create a kernel descriptor for the reader kernel
    reader_kernel_descriptor = ttnn.KernelDescriptor(
        kernel_source=kernel_path("tt_reader.cpp"),
        core_ranges=core_grid,
        compile_time_args=reader_compile_time_args,
        runtime_args=[[reader_rt_args]],
        config=ttnn.ReaderConfigDescriptor(),
    )
    writer_kernel_descriptor = ttnn.KernelDescriptor(
        kernel_source=kernel_path("tt_writer.cpp"),
        core_ranges=core_grid,
        compile_time_args=writer_compile_time_args,
        runtime_args=[[writer_rt_args]],
        config=ttnn.WriterConfigDescriptor(),
    )
    
    compute_kernel_descriptor = ttnn.KernelDescriptor(
        kernel_source=kernel_path("tt_eltwise_sfpu.cpp"),
        core_ranges=core_grid,
        compile_time_args=compute_compile_time_args,
        defines=[],
        runtime_args=[[[]]],
        config=ttnn.ComputeConfigDescriptor(),
    )

    program_descriptor = ttnn.ProgramDescriptor(
        kernels=[reader_kernel_descriptor, writer_kernel_descriptor, compute_kernel_descriptor],
        semaphores=[],
        cbs=[in_cb_descriptor, out_cb_descriptor],
    )

    return program_descriptor

def test_new_op():
    device = ttnn.open_device(device_id=0)

    num_tiles = 4
    src_bank_id = 0
    dst_bank_id = 0

    shape = [1, num_tiles, 32, 32]
    data = torch.rand(shape).to(torch.bfloat16)

    dram_memory_config = ttnn.DRAM_MEMORY_CONFIG

    input_tensor = ttnn.from_torch(data, dtype=ttnn.bfloat16, layout=ttnn.TILE_LAYOUT, device=device, memory_config=dram_memory_config)
    output_tensor = ttnn.allocate_tensor_on_device(ttnn.Shape(shape), ttnn.bfloat16, ttnn.TILE_LAYOUT, device, dram_memory_config)
    
    io_tensors = [input_tensor, output_tensor]

    program_descriptor = prepare_newop_program(device, input_tensor, output_tensor, num_tiles, src_bank_id, dst_bank_id)

    output = ttnn.generic_op(io_tensors, program_descriptor)
    golden = ttnn.exp(input_tensor)

    torch_golden = ttnn.to_torch(golden)
    torch_output = ttnn.to_torch(output)
    logger.info(f"input_tensor: {input_tensor}")
    logger.info(f"torch_golden: {torch_golden}")
    logger.info(f"torch_output: {torch_output}")

    matching = torch.allclose(torch_golden, torch_output)
    logger.info(f"Tensors are matching: {matching}")
    assert matching

    ttnn.close_device(device)


if __name__ == "__main__":
    test_new_op()