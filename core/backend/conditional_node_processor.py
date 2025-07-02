import os
import logging

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
        logger.debug(f"Processing CONDITIONAL node: {node}")
        
        node_data = replay.state.execution.epic.graph.nodes[node]
        contents = node_data.get('contents', {})

        iteration_count = contents.get('iteration_count', 0)
        iteration_max = contents.get('iteration_max', 3)
        if iteration_count >= iteration_max:
            logger.info(f"Conditional iteration limit reached: {iteration_count}/{iteration_max}")

        run_node_id = contents.get('run_node_id', None)
        if run_node_id is None:
            raise ValueError(f"run_node_id is required for CONDITIONAL node {node}")
        run_node = replay.state.execution.epic.graph.nodes[run_node_id]
        run_node_contents = run_node.get('contents', {})
        run_exit_code = run_node_contents.get('exit_code', None)
        if run_exit_code is None:
            raise ValueError(f"exit_code is required for CONDITIONAL node {node}")

        contents['condition'] = run_exit_code == 0
        logger.info(f"Condition evaluated to: {contents['condition']}")
        
        # Log iteration info
        logger.info(f"Conditional iteration {iteration_count}/{iteration_max}")
        
        # The actual branching logic is handled by the execution engine
        # This processor just updates the condition state 