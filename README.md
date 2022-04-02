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
conda env create -f /path/to/environment.yml
```
2) List the urls of the youtube videos you wish to download to "data/music_list.txt" file
3) Define the path to your music directory to the "config/config.cfg" file
In case you don't define it or the path you write there is invalid, the songs will be downloaded to your home directory
4) Launch the program
```bash
python -m /path/to/package
```
PS : in case something goes wrong, find more details from the "log/app.log" file

## Contributing
Pull requests are welcome.

## Support

For any question or assistance needed regarding the use of this package, you can contact me at matthieu.daviaud@gmail.com

## License
[MIT](https://choosealicense.com/licenses/mit/)