## This is the Web Video Parser (and downloader) - UWVP

PLEASE, BEFORE USAGE, READ THE DOCUMENTATION IN FULL!!! <br />

# Instalation

Recommended using python versions 3.10+ <br />
You can install python's latest version for Windows on [python.org](https://python.org/downloads/windows/) <br />
If you are on Linux, I guess, you know how to use python :) <br />

The instalation with git: <br />

```bash
1. $ git clone https://github.com/fascot/Web-Video-Parser/
2. $ cd Web-Video-Parser
3. $ python -m pip install -r requirements.txt
```

Also, you have to download the `ffmeg` on your machine from this [repository](https://github.com/BtbN/FFmpeg-Builds/releases)
If you are on Windows `ffmpeg` has to be installed into PATH. You can read this [article](https://windowsloop.com/install-ffmpeg-windows-10/#add-ffmpeg-to-Windows-path)
If you are on Linux, just use Pacman or Apt:
```bash
1. $ sudo pacman -S ffmpeg 'for Manjaro Linux'
2. $ sudo apt-get install ffmpeg 'for Ubuntu'
```

It's used for output files processing

Downloading code files and libraries Done! <br />

# Usage

You can type commands in no particular order <br />
Except `--help` and `--info`, they have to stand as shown in the table and no commands after them will be used. <br />
Also, `--help` doesn't get url. <br />

Then, don't type one command twice, only first will be used. <br />

Base commands, wich work with any type of url: <br />
```bash
+----------------+-----+------------------+---------------------------------+------------------------------------------------+
| Tool           | Url | Command          | Argument                        | Description                                    |
+----------------+-----+------------------+---------------------------------+------------------------------------------------+
| python uwvp.py | no  | --help           | all | youtube | pornhub | other | Returns documentation for input item           |
| -------------- | url | --info           |                                 | Returns information about page                 |
| -------------- | --- | -n | -name       | custom_name                     | Changes the name of the output media file      |
| -------------- | --- | -p | -path       | custom_path                     | Changes the path of the output media file      |
```

Commands `-o` and `-r` work only with youtube and pornhub links:
```bash
| -------------- | --- | -o | -option     | video_only | audio_only         | Deletes audio or video from output media file  |
| -------------- | --- | -r | -resolution | 144 | 240 | .... | 2160         | Changes resolution of the output media file    |
```

And command `-i` works only with unsupported sites, which has no API, then algorithm gets all video links from site and returns
indexes for media with `--info` command:
```bash
| -------------- | --- | -i | -index      | index                           | Choosing the media file link from site by index |
```

# Thanks To The Developers Of

Pytube <br />
BeautifulSoup4 <br />
Youtube-dl <br />
Pornhub-api <br />
Requests <br />
...