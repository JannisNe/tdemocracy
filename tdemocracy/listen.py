import logging
from collections.abc import Generator
from typing import Any

from hop import Stream
from hop.auth import Auth
from hop.io import StartPosition
from packaging.version import Version

from tdemocracy import __version__ as tdemocracy_version_str
from tdemocracy.model import NuclearTransientReport
from tdemocracy.settings import Settings

LOGGER = logging.getLogger(__name__)


def listen_to_nuclear_stream(
    start_at: Any = StartPosition.EARLIEST,
    until_eos: bool = False,
    settings: Settings | None = None,
) -> Generator[NuclearTransientReport]:
    """
    Listen to Nuclear stream, converts older data model versions to current format if possible.

    :param start_at: where to start the stream, either of StartPosition.EARLIEST or StartPosition.LATEST
    :type start_at: Any
    :param until_eos: Stop loop when the end of the stream is reached or wait for next message (default)
    :type until_eos: bool
    :param settings: Settings to use, if not passed reads the corresponding from the environment or a `.env` file. See :class:`tdemocracy.settings.Settings` for details.
    :type settings: Settings | None
    """
    _settings = settings or Settings()
    auth = Auth(_settings.username, _settings.password.get_secret_value())
    stream = Stream(auth=auth, start_at=start_at, until_eos=until_eos)
    tdemocracy_version = Version(tdemocracy_version_str)

    with stream.open(f"kafka://kafka.scimma.org/{_settings.topic}", mode="r", group_id=_settings.group_id) as s:
        LOGGER.info(f"Listening to {_settings.topic}...")
        for message in s:
            LOGGER.debug("Received message")
            content = message.content
            mv_str = content["model_version"]

            if mv_str in {"0.0.7", "0.0.6", "0.0.5"}:
                yield NuclearTransientReport.model_validate(content)

            elif mv_str in {"0.0.4", "0.0.3", "0.0.2", "0.0.1"}:
                # backwards compatibility for older model version
                content["host"]["ra"] = float("nan")
                content["host"]["dec"] = float("nan")
                content["host"]["sources"] = content["host"]["source"]
                content["host"]["primary_source"] = content["host"]["source"][0]
                yield NuclearTransientReport.model_validate(content)

            elif Version(mv_str) > tdemocracy_version:
                # raise error if latest version is not installed
                msg = (
                    f"Received model version v{mv_str}, installed version v{tdemocracy_version}. "
                    f"Please update tdemocracy!"
                )
                raise ValueError(msg)

            else:
                msg = f"Can not parse model_version: {mv_str}!"
                raise ValueError(msg)
