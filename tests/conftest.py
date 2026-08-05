import json
from contextlib import contextmanager

import pytest
from data.make_test_data import TEST_MESSAGES_PATH
from hop.io import Stream


class Message:
    def __init__(self, content):
        self.content = content


@pytest.fixture(autouse=True)
def messages(monkeypatch):
    with open(TEST_MESSAGES_PATH) as f:
        contents = json.load(f)

    def gen_messages(*args, **kwargs):
        for c in contents:
            yield Message(content=c)

    @contextmanager
    def patch_open(*args, **kwargs):
        yield gen_messages()

    monkeypatch.setattr(Stream, "open", patch_open)
