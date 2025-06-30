import json

class MockAnthropicClient:
    def __init__(self):
        self.captured_jsons = []
        self.messages = self.Messages(self)

    class Messages:
        def __init__(self, parent):
            self.parent = parent
        def create(self, **kwargs):
            json_str = kwargs['messages'][0]['content']
            print(f"\n=== MOCK CLIENT RECEIVED REQUEST ===")
            print(f"Raw JSON: {json_str}")
            try:
                parsed_json = json.loads(json_str)
                print(f"Parsed JSON: {json.dumps(parsed_json, indent=2)}")
                print(f"Prompt: {parsed_json.get('prompt', 'No prompt found')}")
                print(f"Code to edit: {parsed_json.get('code_to_edit', [])}")
                print(f"Read only files: {[f['path_and_filename'] for f in parsed_json.get('read_only_files', [])]}")
                print(f"=== END REQUEST ===\n")
            except Exception as e:
                print(f"Error parsing JSON: {e}")
            
            self.parent.captured_jsons.append(json.loads(json_str))
            class DummyContent:
                def __init__(self, text):
                    self.text = text
            class DummyResponse:
                def __init__(self):
                    code_to_edit = parsed_json.get('code_to_edit', [])
                    response_json = {
                        "files": []
                    }
                    for code_to_edit in code_to_edit:
                        response_json["files"].append({
                            "path_and_filename": code_to_edit["path_and_filename"],
                            "contents": f'# Modified by LLM: {code_to_edit["contents"]}'
                        })

                    self.content = [DummyContent(json.dumps(response_json))]
            return DummyResponse() 