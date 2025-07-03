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
        logger.info(f"Processed EXIT node")