import os

import pytest
from beartype import beartype
from beartype.typing import Callable


@pytest.fixture
@beartype
def create_config_file() -> Callable:
    """Factory fixture to create a custom config file."""

    def _create_config(config_dir: str, content: str) -> str:
        """Create a config.cfg in the specified folder.

        :param config_dir: Path to the config directory
        :type config_dir: str
        :param content: Content to write in the config file
        :type content: str
        :return: Path to the created config file
        :rtype: str
        """
        config_file = os.path.join(config_dir, "config.cfg")
        with open(config_file, "w") as f:
            f.write(content)
        return config_file

    return _create_config
