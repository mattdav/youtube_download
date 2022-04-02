"""Main module collecting configuration and lauching the program"""
import logging
import os
import importlib.resources
from pathlib import WindowsPath
from bin import utils


def get_folder_path(foldername: str) -> WindowsPath:
    """Get path to a package directory from its name

    :param foldername: Name of the directory
    :type foldername: str
    :raises e: If directory doesn't exist, raise a NameError
    :return: Path to the specified directory
    :rtype: WindowsPath
    """
    try:
        with importlib.resources.path(foldername, "__init__.py") as p:
            folder_path = os.path.dirname(p)
    except NameError as e:
        logging.error(f"The directory {foldername} doesn't exist.")
        raise e
    return folder_path


if __name__ == "__main__":
    log_path = get_folder_path("log")
    data_path = get_folder_path("data")
    config_path = get_folder_path("config")
    logging.basicConfig(
        filename=os.path.join(log_path, "app.log"),
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )
    music_path = utils.get_music_path(config_path)
    urls = utils.read_file(os.path.join(data_path, "music_list.txt"))
    utils.process_urls(urls, music_path)
