import logging
from collections.abc import Generator
from typing import Any

from hop import Stream
from hop.auth import Auth
from hop.io import StartPosition

from tdemocracy.model import LSSTReport
from tdemocracy.settings import Settings

LOGGER = logging.getLogger(__name__)


def listen_to_nuclear_stream(
    start_at: Any = StartPosition.EARLIEST,
    until_eos: bool = False,
    settings: Settings | None = None,
) -> Generator[LSSTReport]:
    """
    Listen to Nuclear stream

    :param start_at: where to start the stream, either of StartPosition.EARLIEST or StartPosition.LATEST
    :type start_at: Any
    :param until_eos: Stop loop when the end of the stream is reached or wait for next message (default)
    :type until_eos: bool
    :param settings: Settings to use, if not passed reads the corresponding from the environment or a `.env` file. See :class:`tdemocracy.settings.Settings` for details.
    :type settings: Settings | None

    """
    _settings = settings or Settings()
    auth = Auth(_settings.username, _settings.password)
    stream = Stream(auth=auth, start_at=start_at, until_eos=until_eos)

    with stream.open(f"kafka://kafka.scimma.org/{_settings.topic}", mode="r", group_id=_settings.group_id) as s:
        LOGGER.info(f"Listening to {_settings.topic}...")
        for message in s:
            LOGGER.debug(f"Received message: {message.value}")
            yield LSSTReport.model_validate(message.content)
