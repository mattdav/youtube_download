"""Main module collecting configuration and lauching the program"""

import importlib.resources
import logging
import os
import threading
import tkinter as tk
from tkinter import Tk, filedialog, messagebox, ttk

from beartype import beartype

from .bin.utils import download_url, get_music_path, validate_url


class AppWindow(Tk):
    """Application window with file path tracking."""

    def __init__(self) -> None:
        super().__init__()
        self.file_path: str | None = None
        self.title("Télécharger des musiques depuis YouTube")
        self.geometry("500x250")


@beartype
def get_folder_path(foldername: str) -> str:
    """Get path to a package directory from its name

    :param foldername: Name of the directory
    :type foldername: str
    :raises e: If directory doesn't exist, raise a NameError
    :return: Path to the specified directory
    :rtype: str
    """
    try:
        with importlib.resources.path(foldername, "__init__.py") as p:
            folder_path = os.path.dirname(p)
    except NameError as e:
        logging.error(f"The directory {foldername} doesn't exist.")
        raise e
    return folder_path


def open_file_dialog() -> None:
    """Open a GUI to select the text file containing URLs."""
    file_path = filedialog.askopenfilename(
        title="Sélectionner le fichier à traiter",
        filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
    )
    if file_path.endswith(".txt"):
        file_label.config(text=f"Fichier : {file_path}")
        start_button.config(state=tk.NORMAL)
        window.file_path = file_path
    else:
        messagebox.showerror(
            "Erreur", f"Le fichier {file_path} n'est pas un fichier texte."
        )


def process_urls(urls: list[str]) -> list[str]:
    """
    Validate if URLs are correct youtube ones and rewrite them if
    they contain playlist link.

    :param urls: URLs to process.
    :type urls: list
    :return: Correct URLs.
    :rtype: list
    """
    valid_urls = []
    invalid_urls = []
    for url in urls:
        if validate_url(url):
            if "&list=" in url:
                url = url.split("&list=")[0]
            valid_urls.append(url)
        else:
            invalid_urls.append(url)
    if len(invalid_urls) > 0:
        messagebox.showwarning(
            "Attention",
            "Les URLs suivantes ne sont pas valides et seront ignorées :\n"
            + "\n".join(invalid_urls),
        )
    return list(set(valid_urls))


@beartype
def read_urls_from_file(file_path: str) -> list[str]:
    """
    Read file and return list of URLs.

    :param file_path: Path to the text file.
    :type file_path: str
    :return: List of URLs.
    :rtype: list
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
            urls = process_urls(urls)
            print(urls)
        return urls
    except ValueError as e:
        messagebox.showerror("Erreur", f"Impossible de lire le fichier : {e}")
        return []


def download_with_progress(urls: list[str], music_path: str) -> None:
    """
    Download URLs and update the progress bar accordingly.

    :param urls: List of URLs to download.
    :type urls: list
    :param music_path: Path to the music folder to place downloaded files.
    :type music_path: str
    """
    total = len(urls)
    pbar["maximum"] = total
    pbar["value"] = 0
    progress_label.config(text=f"Traitement : 0/{total}")
    try:
        for idx, url in enumerate(urls, 1):
            download_url(url, music_path)
            pbar["value"] = idx
            progress_label.config(text=f"Traitement : {idx}/{total}")
            window.update_idletasks()
        messagebox.showinfo("Succès", "Tous les fichiers ont été téléchargés !")
    except ValueError as e:
        messagebox.showerror("Erreur", f"Erreur lors du téléchargement : {e}")
    finally:
        open_button.config(state=tk.NORMAL)
        start_button.config(state=tk.NORMAL)


def process_downloads(music_path: str) -> None:
    """
    Start the download process in a separate thread.

    :param music_path: Path to the music folder to place downloaded files.
    :type music_path: str
    """
    file_path = getattr(window, "file_path", None)
    if not file_path:
        messagebox.showwarning("Attention", "Veuillez d'abord charger un fichier!")
        return
    urls = read_urls_from_file(file_path)
    if not urls:
        messagebox.showwarning(
            "Attention", "Le fichier ne contient aucune URL valide !"
        )
        return
    open_button.config(state=tk.DISABLED)
    start_button.config(state=tk.DISABLED)
    thread = threading.Thread(target=download_with_progress, args=(urls, music_path))
    thread.daemon = True
    thread.start()


if __name__ == "__main__":
    log_path = get_folder_path("log")
    logging.basicConfig(
        filename=os.path.join(log_path, "app.log"),
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )
    config_path = get_folder_path("config")
    music_path = get_music_path(config_path)
    window = AppWindow()
    file_frame = ttk.Frame(window, padding=10)
    file_frame.pack(fill=tk.X)
    open_button = ttk.Button(
        file_frame, text="Charger fichier", command=open_file_dialog
    )
    open_button.pack(side=tk.LEFT, padx=5)
    file_label = ttk.Label(
        file_frame, text="Aucun fichier sélectionné", foreground="gray"
    )
    file_label.pack(side=tk.LEFT, padx=10)
    progress_frame = ttk.Frame(window, padding=10)
    progress_frame.pack(fill=tk.X)
    progress_label = ttk.Label(progress_frame, text="Prêt")
    progress_label.pack(anchor=tk.W)
    pbar = ttk.Progressbar(progress_frame, mode="determinate", length=400)
    pbar.pack(fill=tk.X, pady=5)
    button_frame = ttk.Frame(window, padding=10)
    button_frame.pack(fill=tk.X)
    start_button = ttk.Button(
        button_frame,
        text="Démarrer le téléchargement",
        command=lambda: process_downloads(music_path),
        state=tk.DISABLED,
    )
    start_button.pack(side=tk.LEFT, padx=5)
    quit_button = ttk.Button(button_frame, text="Quitter", command=window.quit)
    quit_button.pack(side=tk.LEFT, padx=5)
    window.mainloop()
