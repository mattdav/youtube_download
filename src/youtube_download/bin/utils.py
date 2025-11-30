"""Utilities used by the program"""

import configparser
import logging
import os
import re
import warnings
from pathlib import Path
from typing import Any

import yt_dlp
from beartype import beartype

warnings.filterwarnings("ignore")
log = logging.getLogger(__name__)


@beartype
def validate_url(url: str) -> bool:
    """Check if the input looks like a valid url from youtube via regex

    :param url: input url wrote in the input file music_list.txt
    :type url: str
    :return: True/False
    :rtype: bool

    >>> validate_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    True
    >>> validate_url("https://www.invalidurl.com/watch?v=dQw4w9WgXcQ")
    False
    >>> validate_url("just some random text")
    False
    """
    pattern = r"https://www.youtube.com/watch\?v=*"
    if re.match(pattern, url):
        return True
    else:
        return False


@beartype
def get_music_path(config_path: str) -> str:
    """Get the path to the user's music directory as defined in the config.cfg file
    If the directory doesn't exist, return the home's path instead

    :param config_path: Path to the config folder where the config.cfg file is located
    :type config_path: str
    :raises e: Raise a FileNotFoundError is the config.cfg file doesn't exist
    :raises e: Raise a KeyError if the config.cfg file is not correctly filled
    :return: Return either the path read from the config.cfg file or the home path
    :rtype: str
    """
    config = configparser.RawConfigParser()
    config_file = os.path.join(config_path, "config.cfg")
    if not os.path.exists(config_file):
        logging.error(
            f"The file config.cfg doesn't exist in the directory {config_path}."
        )
        raise FileNotFoundError(f"config.cfg not found in {config_path}")
    config.read(config_file)
    try:
        music_path = config["CONFIG"]["music_path"]
    except KeyError as e:
        logging.error(
            "The config file is not correctly filled.",
            exc_info=True,
        )
        raise e
    if os.path.exists(music_path):
        return music_path
    else:
        return str(Path.home())


@beartype
def download_url(video_url: str, music_path: str) -> None:
    """Download the song of the youtube video and store it to the music directory
    as defined in the config file

    :param video_url: Url of the youtube video
    :type video_url: str
    :param music_path: Path to the user's music directory
    :type music_path: str
    """
    try:
        ydl_opts: dict[str, Any] = {
            "quiet": True,
            "no-warnings": True,
            "outtmpl": f"{music_path}/%(title)s.%(ext)s",
            "postprocessors": [
                {  # Post-process to convert to MP3
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",  # Convert to mp3
                    "preferredquality": "0",  # '0' means best quality
                }
            ],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore[arg-type]
            ydl.download([video_url])
    except Exception as e:
        log.error(f"Failed to download {video_url}", exc_info=True)
        raise e
