## This is the Ultimate Web Video Parser - UWVP

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

Also, you have to download the `ffmpeg` on your machine. <br />

If you are on Windows you have get the latest build version for Windows from this [repository](https://github.com/BtbN/FFmpeg-Builds/releases).
And `ffmpeg` has to be installed into PATH. You can read this [article](https://windowsloop.com/install-ffmpeg-windows-10/#add-ffmpeg-to-Windows-path) with information how to do it. <br />

If you are on Linux, just use Pacman or Apt:
```bash
1. $ sudo pacman -S ffmpeg        'for Manjaro Linux'
2. $ sudo apt-get install ffmpeg  'for Ubuntu'
```

`ffmpeg` is using for output media processing.


Downloading code files and libraries Done! <br />

# Usage

IMPORTANT: `--help` does not work yet, use documentation. <br />

You can type commands in no particular order <br />
Except `--help` and `--info`, they have to stand as shown in the table and no commands after them will be used. <br />
Also, `--help` doesn't get url. <br />

Then, don't type one command twice, only first will be used. <br />

Base commands, wich work with any type of url: <br />
```bash
| Tool           | Url | Command          | Argument                        | Description                                    |
+----------------+-----+------------------+---------------------------------+------------------------------------------------+
| python uwvp.py |     | --help           | all | youtube | unknown_site... | Returns documentation for input item           |
| python uwvp.py | url | --info           |                                 | Returns information about page                 |
| python uwvp.py | url | -n | -name       | custom_name                     | Changes the name of the output media file      |
| python uwvp.py | url | -p | -path       | custom_path                     | Changes the path of the output media file      |
```

Commands `-o` and `-r` work only with youtube and pornhub links:
```bash
| python uwvp.py | url | -o | -option     | video_only | audio_only         | Deletes audio or video from output media file  |
| python uwvp.py | url | -r | -resolution | 144 | 240 | .... | 2160         | Changes resolution of the output media file    |
```

And command `-i` works only with unsupported sites, which has no API, and algorithm gets all video links from site and returns
indexes for media with `--info` command:
```bash
| python uwvp.py | url | -i | -index      | index                           | Choosing the media file link from site by index |
```

BY DEFAULT:

 - video from youtube and pornhub downloads in the highest quality <br />
 - video from youtube and pornhub downloads with video and audio <br />
 - name for output media from unknown sites generates randomly <br />
 - name for output media from youtube and pornhub generates by video title <br />
 - path for output media is in the directory where the script installed <br />
 - index for media from unknown site is None, means that with no given index you'll get the exception <br />

# Plans

- Bug fixes and adding features for already supported sites <br />
- Trying to use Selenium to get media files by doing activity on site <br />
- Also making configs for sites which have no media links on page by default (Selenium automatization) <br />
- Make builds for each os, to not using `python uwvp.py` every time
- GUI for average users

# Thanks To The Developers Of

Pytube <br />
BeautifulSoup4 <br />
Youtube-dl <br />
Pornhub-api <br />
Requests <br />
...
