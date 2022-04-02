"""Utilities used by the program"""
import configparser
from pathlib import WindowsPath
import os
import logging
import youtube_dl
from youtube_dl.utils import DownloadError
import string
from pathlib import Path
import re

log = logging.getLogger(__name__)


def url_validator(url: str) -> bool:
    """Check if the input looks like a valid url from youtube via regex

    :param url: input url wrote in the input file music_list.txt
    :type url: str
    :return: True/False
    :rtype: bool
    """
    pattern = "(http|https)://www.youtube.com/watch\?v=*"
    if re.match(pattern, url):
        return True
    else:
        return False


def get_music_path(config_path: WindowsPath) -> str:
    """Get the path to the user's music directory as defined in the config.cfg file
    If the directory doesn't exist, return the home's path instead

    :param config_path: Path to the config folder where the config.cfg file is located
    :type config_path: WindowsPath
    :raises e: Raise a FileNotFoundError is the config.cfg file doesn't exist
    :raises e: Raise a KeyError if the config.cfg file is not correctly filled
    :return: Return either the path read from the config.cfg file or the home path
    :rtype: str
    """
    config = configparser.RawConfigParser()
    try:
        config.read(os.path.join(config_path, "config.cfg"))
    except FileNotFoundError as e:
        logging.error(
            f"The file config.cfg doesn't exist in the directory {config_path}."
        )
        raise e
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
        return Path.home()


def read_file(file_path: WindowsPath) -> list:
    """Read text file from path, used to read the list of url to download defined in the music_list.txt
    file which is in the data directory

    :param file_path: Path to the file
    :type file_path: WindowsPath
    :raises e: Raise a FileNoyFoundError if the file doesn't exist
    :return: Return the list of urls wrote in the music_list.txt file
    :rtype: list
    """
    try:
        with open(file_path) as f:
            content = f.readlines()
    except FileNotFoundError as e:
        logging.error(
            "The file music_list.txt doesn't exist in the data folder.",
            exc_info=True,
        )
        raise e
    nb_music = len(content)
    logging.info(f"{nb_music} songs to download.")
    return content


def download_url(video_url: str, music_path: WindowsPath) -> WindowsPath:
    """Download the song of the youtube video and store it to the music directory as defined in the
    config file

    :param video_url: Url of the youtube video
    :type video_url: str
    :param music_path: Path to the user's music directory
    :type music_path: WindowsPath
    :return: Return the path to the downloaded file
    :rtype: WindowsPath
    """
    try:
        video_info = youtube_dl.YoutubeDL().extract_info(url=video_url, download=False)
        video_title = video_info["title"].translate(
            str.maketrans("", "", string.punctuation)
        )
        filename = f"{video_title}.wav"
        output_path = os.path.join(music_path, filename)
        if not os.path.isfile(output_path):
            options = {
                "quiet": True,
                "noplaylist": True,
                "format": "bestaudio/best",
                "keepvideo": False,
                "outtmpl": output_path,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "wav",
                        "preferredquality": "192",
                    }
                ],
            }
            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([video_url])
        return output_path
    except DownloadError:
        logging.error(f"Url '{video_url}' not found.")
        pass


def convert_file(old_file: WindowsPath, new_file: WindowsPath):
    """Convert file from wav to mp3

    :param old_file: Path to the wav file
    :type old_file: WindowsPath
    :param new_file: Path to the mp3 file
    :type new_file: WindowsPath
    """
    os.system(f"""ffmpeg -i "{old_file}" -vn -ar 44100 -ac 2 -b:a 192k "{new_file}""")


def remove_file(file: WindowsPath):
    """Delete file

    :param file: File's path
    :type file: WindowsPath
    """
    os.remove(file)


def process_urls(urls: list, music_path: WindowsPath):
    """For each url in the list, download the song from the youtube video, convert it from wav to mp3
    and delete the former one

    :param urls: Url of the youtube video
    :type urls: list
    :param music_path: Path to the user's music directory
    :type music_path: WindowsPath
    """
    for url in urls:
        try:
            assert url_validator(url)
            wav = download_url(url, music_path)
            mp3 = Path(wav).stem + ".mp3"
            convert_file(wav, os.path.join(music_path, mp3))
            remove_file(wav)
            logging.info(f"Fichier {mp3} créé.")
        except AssertionError:
            logging.error(f"Input {url} is not a youtube url.")
            pass
