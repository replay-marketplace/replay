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
            self.parent.captured_jsons.append(json.loads(json_str))
            class DummyResponse:
                def __init__(self):
                    self.content = [{"text": json.dumps({"files": [{"path_and_filename": "dummy.txt", "contents": "dummy content"}]})}]
            return DummyResponse() 