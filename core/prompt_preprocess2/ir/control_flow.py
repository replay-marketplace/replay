from loguru import logger
from .ir import EpicIR, Opcode


def debug_print(message: str, indent: int = 0, DEBUG: bool = True):
    if DEBUG:
        print(" " * indent + message)


def cfg_traversal_init_queue(epic: EpicIR) -> list:
    queue = []
    queue.append(epic.first_node)
    return queue


def cfg_traversal_step(epic: EpicIR, queue: list) -> tuple[list, str]:
    DEBUG = True
    INDENT = 2
    
    if len(queue) == 0:
        return queue, None

    current_node = queue.pop()
    debug_print(f"\nCurrent node: {current_node}", INDENT, DEBUG)
    
    # Check if the node is a CONDITIONAL node
    if epic.graph.nodes[current_node]['opcode'] == Opcode.CONDITIONAL:
        # See replay.py and conditional_node_processor.py
        # We are currently handling CONDITIONAL nodes in the processor
        # Letting processor set the next node and update the queue
        pass
            
    # All other nodes
    else:
        successors = list(epic.graph.successors(current_node))
        debug_print(f"Adding successors to queue: {successors}", INDENT + 2, DEBUG)
        queue.extend(successors)
    
    
    debug_print(f"Current queue: {queue}", INDENT + 2, DEBUG)

    return queue, current_node 