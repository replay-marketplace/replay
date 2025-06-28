import os
import json
import pytest
from prompt_preprocess2.ir.ir import Opcode
from replay import replay
import logging

class MockAnthropicClient:
    def __init__(self):
        self.captured_jsons = []
        self.messages = self.Messages(self)

    class Messages:
        def __init__(self, parent):
            self.parent = parent
        def create(self, **kwargs):
            json_str = kwargs['messages'][0]['content']
            self.parent.captured_jsons.append(json.loads(json_str))
            class DummyResponse:
                def __init__(self):
                    self.content = [{"text": json.dumps({"files": []})}]
            return DummyResponse()

def test_llm_json_formation_with_mock(tmp_path):
    # Use statically created test resources
    test_dir = os.path.dirname(__file__)
    resources_dir = os.path.join(test_dir, "llm_json_resources")
    docs_dir = os.path.join(resources_dir, "docs")
    template_dir = os.path.join(resources_dir, "template")
    prompt_file = os.path.join(resources_dir, "prompt.txt")

    # Prepare replay_output dir
    replay_output = tmp_path / "replay_output"
    replay_output.mkdir()

    logging.info(f"docs_dir: {docs_dir}")
    logging.info(f"template_dir: {template_dir}")
    logging.info(f"prompt_file: {prompt_file}")
    logging.info(f"replay_output: {replay_output}")

    # Use the normal mock client
    mock_client = MockAnthropicClient()

    # Run the real replay pipeline
    replay(prompt_file, "project", str(replay_output), client=mock_client)

    # Check the captured JSONs
    captured_jsons = mock_client.captured_jsons
    assert len(captured_jsons) == 2
    assert captured_jsons[0]['prompt'].startswith('This is prompt 1')
    assert captured_jsons[1]['prompt'].startswith('This is prompt 2')
    # Check code_to_edit and read_only_files contents
    assert any(f['path_and_filename'] == 'code1.py' for f in captured_jsons[0]['code_to_edit'])
    assert any(f['path_and_filename'] == 'doc1.txt' for f in captured_jsons[0]['read_only_files'])
    assert any(f['path_and_filename'] == 'tmpl1.txt' for f in captured_jsons[0]['read_only_files'])
    assert any(f['path_and_filename'] == 'code2.py' for f in captured_jsons[1]['code_to_edit'])
    assert any(f['path_and_filename'] == 'doc2.txt' for f in captured_jsons[1]['read_only_files'])
    assert any(f['path_and_filename'] == 'tmpl2.txt' for f in captured_jsons[1]['read_only_files']) 