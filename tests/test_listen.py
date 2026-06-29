import logging

from hop import Stream
from hop.auth import Auth
from hop.io import StartPosition

from tdemocracy.model import LSSTReport
from tdemocracy.settings import Settings

LOGGER = logging.getLogger(__name__)


def test_listen_to_nuclear_stream(tmp_path):
    logging.basicConfig(level=logging.DEBUG)
    _settings = Settings()
    auth = Auth(_settings.username, _settings.password)
    stream = Stream(auth=auth, start_at=StartPosition.EARLIEST, until_eos=True)

    messages = []
    with stream.open(f"kafka://kafka.scimma.org/{_settings.topic}", mode="r", group_id=_settings.group_id) as s:
        LOGGER.info(f"Listening to {_settings.topic}...")
        for message in s:
            LOGGER.debug("Received message")
            messages.append(message)

    LOGGER.info(f"Received {len(messages)} messages")
    assert len(messages) > 0

    for m in messages[-2:]:
        assert LSSTReport.model_validate(m.content) is not None
