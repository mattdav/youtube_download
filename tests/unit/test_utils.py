import os
from pathlib import Path, WindowsPath

import pytest
from beartype.typing import Callable
from src.youtube_download.bin import utils

dir_path = os.path.dirname(os.path.realpath(__file__))


def test_get_music_path_with_valid_config_file(
    tmp_path: WindowsPath, create_config_file: Callable
) -> None:
    """Test utils.get_music_path with a valid config file.

    :param tmp_path: Path to the temporary directory as string
    :type tmp_path: WindowsPath
    :param create_config_file: Factory fixture to create a custom config file
    :type create_config_file: Callable
    """
    music_dir = tmp_path / "music"
    music_dir.mkdir()
    config_content = f"[CONFIG]\nmusic_path = {music_dir}\n"
    create_config_file(str(tmp_path), config_content)
    result = utils.get_music_path(str(tmp_path))
    assert result == str(music_dir)


def test_get_music_path_with_nonexistent_directory(
    tmp_path: WindowsPath, create_config_file: Callable
) -> None:
    """Test utils.get_music_path with non-existing directory.

    :param tmp_path: Path to the temporary directory as string
    :type tmp_path: WindowsPath
    :param create_config_file: Factory fixture to create a custom config file
    :type create_config_file: Callable
    """
    music_dir = "/fake/nonexistent/path"
    config_content = f"[CONFIG]\nmusic_path = {music_dir}\n"
    create_config_file(str(tmp_path), config_content)
    result = utils.get_music_path(str(tmp_path))
    assert result == str(Path.home())


def test_get_music_path_config_file_not_found(
    tmp_path: WindowsPath, caplog: pytest.LogCaptureFixture
) -> None:
    """Test utils.get_music_path raising FileNotFoundError

    :param tmp_path: Path to the temporary directory as string
    :type tmp_path: WindowsPath
    """
    with pytest.raises(FileNotFoundError, match="config.cfg not found"):
        utils.get_music_path(str(tmp_path))
        assert "The file config.cfg doesn't exist in the directory" in caplog.text


def test_get_music_path_missing_music_path_key(
    tmp_path: WindowsPath,
    create_config_file: Callable,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test utils.get_music_path with invalid config file.

    :param tmp_path: Path to the temporary directory as string
    :type tmp_path: WindowsPath
    :param create_config_file: Factory fixture to create a custom config file
    :type create_config_file: Callable
    :param caplog: Pytest fixture to capture log output
    :type caplog: pytest.LogCaptureFixture
    """
    invalid_config_content = "[OTHER_SECTION]\nkey = value\n"
    create_config_file(str(tmp_path), invalid_config_content)
    with pytest.raises(KeyError):
        utils.get_music_path(str(tmp_path))
        assert "The config file is not correctly filled" in caplog.text
