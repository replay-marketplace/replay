import logging

logger = logging.getLogger(__name__)

class ExitNodeProcessor:
    """Processor for EXIT nodes in the workflow."""
    
    def process(self, replay, node):
        """
        Process an EXIT node.
        
        Args:
            replay: The Replay instance
            node: The node identifier
        """
        logger.debug(f"Processing EXIT node: {node}")
        # EXIT nodes are typically just markers for workflow completion
        # No specific action needed, just log that we've reached the end
        logger.info(f"Workflow completed at EXIT node: {node}") 