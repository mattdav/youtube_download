# youtube_download

Python package to download music from youtube based on a list of urls.

## Installation

Clone the package to your directory
```bash
git clone https://github.com/mattdav/youtube_download.git
```

## Usage

1) Install dependencies listed in the requirements
```bash
uv sync
```
2) List the urls of the youtube videos you wish to download to a text file
3) Define the path to your music directory to the "config/config.cfg" file
In case you don't define it or the path you write there is invalid, the songs will be downloaded to your home directory
4) Launch the program
```bash
python /path/to/package/src/youtube_download
```
PS : in case something goes wrong, the GUI will return errors.

## Contributing
Pull requests are welcome.

## Support

For any question or assistance needed regarding the use of this package, you can contact me at matthieu.daviaud@gmail.com

## License
[MIT](https://choosealicense.com/licenses/mit/)