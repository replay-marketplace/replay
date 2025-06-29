import logging

logger = logging.getLogger(__name__)

class DocNodeProcessor:
    def process(self, replay, node):
        # No-op: Docs copying is handled in preprocessing now
        logger.debug("DocNodeProcessor: no-op (handled in preprocessing)")
        pass 