import os
import shutil
import logging

logger = logging.getLogger(__name__)

class TemplateNodeProcessor:
    def process(self, replay, node):
        # No-op: Template copying is handled in preprocessing now
        logger.debug("TemplateNodeProcessor: no-op (handled in preprocessing)")
        pass 