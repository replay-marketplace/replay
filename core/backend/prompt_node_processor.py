import os
import json
import logging
from pathlib import Path
from core.prompt_preprocess2.ir.ir import Opcode
from core.json_to_code.json_to_code import json_to_code

logger = logging.getLogger(__name__)

class PromptNodeProcessor:
    def process(self, replay, node):
        epic = replay.state.execution.epic
        code_dir = replay.code_dir
        project_dir = replay.project_dir
        replay_dir = replay.replay_dir
        client = replay.client
        system_instructions = replay.system_instructions
        contents = epic.graph.nodes[node]['contents']
        logger.debug(f"Processing prompt: {contents}")
        prompt = self._build_prompt_from_contents(contents, replay_dir)
        code_to_edit_paths = [os.path.join(code_dir, ref) for ref in contents.get('code_refs', [])]
        llm_json = {
            'prompt': prompt,
            'code_to_edit': self._serialize_files_and_dirs(code_dir, code_to_edit_paths),
            'read_only_files': self._serialize_read_only_files(epic, node, contents, project_dir),
            'commands_to_run': []
        }
        llm_json_str = json.dumps(llm_json, indent=4)
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            system=system_instructions,
            messages=[{"role": "user", "content": llm_json_str}],
            max_tokens=4096
        )
        response_json = json.loads(response.content[0].text)
        json_to_code(code_dir, response_json['files'])

    def _build_prompt_from_contents(self, contents, replay_dir):
        if contents.get('terminal_output') is not None:
            terminal_output_file = contents['terminal_output']
            print(f"terminal_output: {terminal_output_file}")
            terminal_output_path = os.path.join(replay_dir, terminal_output_file)
            try:
                with open(terminal_output_path, "r") as f:
                    terminal_output = f.read()
                logger.debug(f"terminal_output: {terminal_output}")
                prompt = f"Fix this error: {terminal_output}"
                logger.debug(f"Processing prompt: {prompt}")
            finally:
                if os.path.exists(terminal_output_path):
                    os.remove(terminal_output_path)
        else:
            prompt = contents.get('prompt', '')
            logger.debug(f"Processing prompt: {prompt}")
        return prompt

    def _serialize_files_and_dirs(self, base_dir, paths):
        result = []
        base_dir = Path(base_dir)
        for rel_path in paths:
            abs_path = base_dir / rel_path
            if abs_path.is_file():
                try:
                    contents = abs_path.read_text(encoding='utf-8')
                    result.append({
                        "path_and_filename": str(rel_path),
                        "contents": contents
                    })
                except Exception as e:
                    logger.error(f"Error reading file {abs_path}: {str(e)}")
            elif abs_path.is_dir():
                for file_path in abs_path.rglob('*'):
                    if file_path.is_file():
                        rel_file_path = file_path.relative_to(base_dir)
                        try:
                            contents = file_path.read_text(encoding='utf-8')
                            result.append({
                                "path_and_filename": str(rel_file_path),
                                "contents": contents
                            })
                        except Exception as e:
                            logger.error(f"Error reading file {file_path}: {str(e)}")
        return result

    def _serialize_read_only_files(self, epic, node, contents, project_dir):
        read_only_files = []
        session_dir = os.path.dirname(project_dir) if project_dir.endswith('latest') else project_dir
        
        # Handle docs references - files come from the docs directory
        docs_refs = contents.get('docs_refs', [])
        if docs_refs:
            docs_dir = os.path.join(session_dir, "docs")
            for ref in docs_refs:
                file_path = os.path.join(docs_dir, ref)
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            contents_text = f.read()
                        read_only_files.append({
                            "path_and_filename": ref,
                            "contents": contents_text
                        })
                        logger.debug(f"Added readonly docs file: {ref}")
                    except Exception as e:
                        logger.error(f"Error reading docs file {file_path}: {str(e)}")
        
        # Handle template references - files come from the template directory
        template_refs = contents.get('template_refs', [])
        if template_refs:
            template_dir = os.path.join(session_dir, "template")
            for ref in template_refs:
                file_path = os.path.join(template_dir, ref)
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            contents_text = f.read()
                        read_only_files.append({
                            "path_and_filename": ref,
                            "contents": contents_text
                        })
                        logger.debug(f"Added readonly template file: {ref}")
                    except Exception as e:
                        logger.error(f"Error reading template file {file_path}: {str(e)}")
        
        # Handle code references - files come from the code directory
        code_refs = contents.get('code_refs', [])
        if code_refs:
            code_dir = os.path.join(session_dir, "code")
            for ref in code_refs:
                file_path = os.path.join(code_dir, ref)
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            contents_text = f.read()
                        read_only_files.append({
                            "path_and_filename": ref,
                            "contents": contents_text
                        })
                        logger.debug(f"Added readonly code file: {ref}")
                    except Exception as e:
                        logger.error(f"Error reading code file {file_path}: {str(e)}")
        
        return read_only_files 