## This is the Ultimate Web Video Parser (and downloader) - UWVP

Please, before usage, read the documentation in full <br />

# Instalation

Recommended using python versions 3.10+ <br />
You can install python's latest version for Windows on [python-site](https://python.org/downloads/windows/) <br />

```bash
1. $ git clone https://github.com/fascot/myproject/
2. $ cd Ultimate-Web-Video-Parser
3. $ python -m pip install -r requirements
```
Downloading code and libraries Done! <br />

# Usage

You can type commands in no particular order, <br />
Except --help and --info, they have to stand as shown in the table and no commands after them will be used. <br />
Also, --help doesn't get url. <br />

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

Commands -o and -r work only with youtube and pornhub links:
```bash
| -------------- | --- | -o | -option     | video_only | audio_only         | Deletes audio or video from output media file  |
| -------------- | --- | -r | -resolution | 144 | 240 | .... | 2160         | Changes resolution of the output media file    |
```

And command -i works only with unsupported sites, which has no API, then algorithm gets all video links from site and returns
indexes for media with --info command:
```bash
| -------------- | --- | -i | -index      | index                           | Choosing the media file link from site by index |
+----------------+-----+------------------+---------------------------------+-------------------------------------------------+
```

# Thanks To The Developers Of

Pytube <br />
BeautifulSoup4 <br />
Youtube-dl <br />
Pornhub-api <br />
Requests <br />
...