
# Youtube download

Python package to download youtube music from a list of urls.


## Authors

- [@mattdav](https://github.com/mattdav)


## Badges

Add badges from somewhere like: [shields.io](https://shields.io/)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![YouTube Music](https://img.shields.io/badge/YouTube_Music-FF0000?style=for-the-badge&logo=youtube-music&logoColor=white)

## Run Locally

Clone the project

```bash
  git clone https://github.com/mattdav/youtube_download.git
```

Go to the project directory

```bash
  cd path_to_youtube_download
```

Create virtual env

```bash
  uv venv
```

Install dependencies

```bash
  uv sync
```

Activate venv

```bash
  .venv\Scripts\activate
```

Run program

```bash
  python src\youtube_download
```


## Environment Variables

To run this project, you will need to add the following environment variables to a config.cfg file placed in src\youtube_download\config (see config.cfg.example) :

`MUSIC_PATH : path to your music folder`




## Usage/Examples

Place URLs you want to download in a text file : 
```text
https://www.youtube.com/watch?v=URL1
https://www.youtube.com/watch?v=URL2
https://www.youtube.com/watch?v=URL3
...
```

Select the file via the GUI when you start program.
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Acknowledgements

 - [yt-dlp](https://pypi.org/project/yt-dlp/)
 - [README generator](https://readme.so/fr)


