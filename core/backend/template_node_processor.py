import os
import shutil
import logging

logger = logging.getLogger(__name__)

class TemplateNodeProcessor:
    def process(self, replay, node):
        epic = replay.epic
        code_dir = replay.code_dir
        template_path = epic.graph.nodes[node]['contents']['path']
        logger.debug(f"Processing template: {template_path}")
        if not os.path.exists(template_path):
            logger.error(f"Template file or directory does not exist: {template_path}")
            raise FileNotFoundError(f"Template path does not exist: {template_path}")
        template_parent = os.path.dirname(template_path)
        rel_template_path = os.path.relpath(template_path, template_parent)
        dest_path = os.path.join(code_dir, rel_template_path)
        try:
            if os.path.isfile(template_path):
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy(template_path, dest_path)
                logger.debug(f"Copied template file to: {dest_path}")
            elif os.path.isdir(template_path):
                shutil.copytree(template_path, dest_path, dirs_exist_ok=True)
                logger.debug(f"Copied template directory to: {dest_path}")
            else:
                logger.error(f"Template path is neither file nor directory: {template_path}")
                raise Exception(f"Unknown template path type: {template_path}")
        except Exception as e:
            logger.error(f"Error copying template: {e}")
            raise 