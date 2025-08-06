import math
import os
import sys
import ttnn

# Make sure we can import prepare_newop_program
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_newop import prepare_newop_program

def ttnn_op(*args, **kwargs):

    """TTNN implementation matching PyTorch signature"""
    # assumes one input, no kwargs
    data = args[0]

    device = ttnn.open_device(device_id=0)

    num_tiles = math.ceil(data.numel() / (32*32))
    src_bank_id = 0
    dst_bank_id = 0

    shape = data.shape

    dram_memory_config = ttnn.DRAM_MEMORY_CONFIG

    input_tensor = ttnn.from_torch(data, dtype=ttnn.bfloat16, layout=ttnn.TILE_LAYOUT, device=device, memory_config=dram_memory_config)
    output_tensor = ttnn.allocate_tensor_on_device(ttnn.Shape(shape), ttnn.bfloat16, ttnn.TILE_LAYOUT, device, dram_memory_config)
    
    io_tensors = [input_tensor, output_tensor]

    program_descriptor = prepare_newop_program(device, input_tensor, output_tensor, num_tiles, src_bank_id, dst_bank_id)

    output = ttnn.generic_op(io_tensors, program_descriptor)
    torch_output = ttnn.to_torch(output, dtype=data.dtype)

    ttnn.close_device(device)

    return torch_output
