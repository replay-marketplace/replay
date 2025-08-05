import os
import logging
from core.prompt_preprocess2.ir.control_flow import cfg_traversal_step

logger = logging.getLogger(__name__)

class ConditionalNodeProcessor:
    """Processor for CONDITIONAL nodes in the workflow."""
    
    def process(self, replay, node):
        """
        Process a CONDITIONAL node by reading the condition file and determining the next step.
        
        Args:
            replay: The Replay instance
            node: The node identifier
        """
        node_id = node.get('id', 'UNKNOWN')
        logger.debug(f"Processing CONDITIONAL node: {node_id}")
        
        contents = node.get('contents', {})

        iteration_count = contents.get('iteration_count', 0)
        iteration_max = contents.get('iteration_max', 3)
        
        # Log current iteration (before increment)
        logger.info(f"Conditional iteration {iteration_count}/{iteration_max}")
        
        if iteration_count > iteration_max:            
            raise ValueError(f"Conditional iteration limit reached: {iteration_count}/{iteration_max}. Should not happen. Control flow graph is broken")

        run_node_id = contents.get('run_node_id', None)
        if run_node_id is None:
            raise ValueError(f"run_node_id is required for CONDITIONAL node {node_id}")
        run_node = replay.state.execution.epic.graph.nodes[run_node_id]
        run_node_contents = run_node.get('contents', {})
        run_exit_code = run_node_contents.get('exit_code', None)
        if run_exit_code is None:
            raise ValueError(f"exit_code is required for CONDITIONAL node {node_id}")
        logger.info(f"Run exit code: {run_exit_code}")

        should_fail = contents.get("should_fail", False)
        if should_fail:
            condition_result = run_exit_code == 1
        else:
            condition_result = run_exit_code == 0


        contents['condition'] = condition_result
        logger.info(f"Condition evaluated to: {condition_result}")

        iteration_count = contents.get('iteration_count', 0)
        iteration_max = contents.get('iteration_max', 5)
        if iteration_count >= iteration_max:
            raise ValueError(f"Conditional iteration limit reached: {iteration_count}/{iteration_max}")

        # Increment the iteration count
        contents['iteration_count'] = iteration_count + 1
        
        next_node = None
        if condition_result:
            next_node = contents['true_node_target']
            logger.info(f"✅ True branch")
        else:
            next_node = contents['false_node_target']
            logger.info(f"❌ False branch")

        queue, next_node = cfg_traversal_step(replay.state.execution.epic, [next_node])
        replay.state.execution.control_flow_graph_queue = queue
        replay.state.execution.current_node_id = next_node
