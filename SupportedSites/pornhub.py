import os
import requests
from bs4 import BeautifulSoup
from pornhub_api import PornhubApi
import youtube_dl
from pathlib import Path


def pornhub_check(url):
    if 'pornhub' in url:
        return True
    return False

def pornhub_get_docs():
    text ='''
+-------------------------+
| Pornhub:                |
+------+------------------+---------------------------+---------------------------------------------------------------+
|      |--info            |                           |  returns avaliable resolutions for video downloading          |
|      |-o / -option      |  video_only / audio_only  |  by dafault downloads video and audio                         |
| url  |-p / -path        |  /full/path               |  by default locates downloads into (path to script)/downloads |
|      |-n / name         |  your_name                |  by default name generates with video title                   |
|      |-r / -resolution  |  144 / 240/ ... / 2160..  |  by default resolution is highest                             |
+------+------------------+---------------------------+---------------------------------------------------------------+
'''
    return text

def pornhub_opt_func_check():
    return True

def pornhub_idx_func_check():
    return False

def pornhub_res_func_check():
    return True

def get_resolutions(url):
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    response = requests.get(url).content
    page = BeautifulSoup(response, 'html.parser')
    script = str(page.find(id = 'player').contents[1].__dict__['contents'][0])

    start_index = script.index('"defaultQuality"')+18
    res_list = ['']
    list_index = 0

    for i in range(32):
        symb = script[start_index + i]
        if symb == ']':
            break
        elif symb in numbers:
            res_list[list_index] += symb
        else:
            list_index += 1
            res_list.append('')

    return res_list

def pornhub_info(url):
    resolutions = ['2160','1440','1080','720','480','360','240']

    if '/view_video.php?viewkey=' in url:
        res_list = get_resolutions(url)

    else:
        print("ERROR: Wrong pornhub link: maybe this link is not a video link, but channel or playlist and etc.")

    api = PornhubApi()
    vid_id = url[url.index('=')+1:]
    video = api.video.get_by_id(vid_id).video
    title = video.title
    text = f"  {title}\n   Avaliable video resolutions: "
    for res in res_list:
        text = f"{text+res}p, "
    text = text[:-2]

    return text

def pornhub_downloader(url, opts):
    resolutions = ['2160','1440','1080','720','480','360','240']
    if custom_path is None:
        output_path = f"{Path().resolve()}/downloads/"
    else:
        output_path = custom_path

    if '/view_video.php?viewkey=' in url:
        if opts['index'] is not None:
            print("WARNING: -i (-index) option will be ignored, use '--help pornhub' too get more info")

        resolution = opts['resolution']
        video_only = opts['video_only']
        audio_only = opts['audio_only']
        custom_path = opts['path']
        custom_name = opts['name']

        if resolution == 'best' or resolution in resolutions or resolution is None:
            if custom_name is None:
                api = PornhubApi()
                vid_id = url[url.index('=')+1:-1] + url[-1]
                video = api.video.get_by_id(vid_id).video
                title = video.title
                title = title.replace(' ', '_')
            else:
                title = custom_name

            if resolution == 'best' or resolution == '':
                format = 'best'
            else:
                format = f'best[height={resolution}]'

            try:
                download_options = {'format': format,
                        'outtmpl': f'{output_path}output.mp4',
                        'ignoreerrors': True,
                        'nowarnings': True,
                        'nooverwrites': True}

                with youtube_dl.YoutubeDL(download_options) as ydl:
                    ydl.download([url])

            except:
                print("ERROR: Couldn't download video: check your url or resolution of video, maybe it's too big")
        else:
            print("ERROR: Invalid resolution optinon: check documentation")
    else:
        print("ERROR: Wrong pornhub link: maybe this link is not a video link, but channel or playlist and etc.")
    
    if video_only:
        cmd = f"ffmpeg -i {output_path}output.mp4 -c:v copy -an {output_path + title}.mp4"
        os.system(cmd)
        return "Video download complete!"
    elif audio_only:
        cmd = f"ffmpeg -i {output_path}output.mp4 -c:a copy -vn {output_path + title}.mp4"
        os.system(cmd)
        return "Audio download complete!"
    else:
        os.rename(f"{output_path}output.mp4", f"{output_path + title}.mp4")
        return "Video and audio download complete!"
