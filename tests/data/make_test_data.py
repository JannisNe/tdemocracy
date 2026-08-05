import json
import logging
from pathlib import Path

from hop.io import Auth, StartPosition, Stream

from tdemocracy.settings import Settings

TEST_MESSAGES_PATH = Path(__file__).parent / "test_messages.json"
LOGGER = logging.getLogger(__name__)


def make_messages():
    LOGGER.info("Making test messages...")
    versions = set()
    messages = []

    _settings = Settings()
    auth = Auth(_settings.username, _settings.password.get_secret_value())
    stream = Stream(auth=auth, start_at=StartPosition.EARLIEST, until_eos=True)

    with stream.open(f"kafka://kafka.scimma.org/{_settings.topic}", mode="r", group_id=_settings.group_id) as s:
        LOGGER.info(f"Listening to {_settings.topic}...")
        for message in s:
            LOGGER.debug("Received message")
            content = message.content

            mv = content["model_version"]
            if mv in versions:
                continue
            LOGGER.info(f"Adding message of model version {mv}")
            versions.add(mv)
            messages.append(content)

    LOGGER.info(f"Got {len(messages)} messages. Writing to {TEST_MESSAGES_PATH}")

    with open(TEST_MESSAGES_PATH, "w") as f:
        json.dump(messages, f)

    LOGGER.info("Done.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    make_messages()
