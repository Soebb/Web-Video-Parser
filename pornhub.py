import os
import requests
from bs4 import BeautifulSoup
from pornhub_api import PornhubApi
import youtube_dl

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
        raise(ValueError, "Wrong pornhub link: maybe this link is not a video link, but channel or playlist and etc.")

    api = PornhubApi()
    vid_id = url[url.index('=')+1:]
    video = api.video.get_by_id(vid_id).video
    title = video.title
    text = f"  {title}\n   Avaliable video resolutions: "
    for res in res_list:
        text = f"{text+res}p, "
    text = text[:-2]

    return text

def pornhub_downloader(url, res, audio_only = False, video_only = False, custom_name = None, custom_path = None):
    resolutions = ['2160','1440','1080','720','480','360','240']
    if custom_path is None:
        video_path = "~/downloads/"
    else:
        video_path = custom_path

    if '/view_video.php?viewkey=' in url:
        if res == 'best' or res in resolutions or res is None:
            if custom_name is None:
                api = PornhubApi()
                vid_id = url[url.index('=')+1:-1] + url[-1]
                video = api.video.get_by_id(vid_id).video
                title = video.title
                title = title.replace(' ', '_')
            else:
                title = custom_name

            if res == 'best' or res == '':
                format = 'best'
            else:
                format = f'best[height={res}]'

            try:
                opts = {'format': format,
                        'outtmpl': f'{video_path}output.mp4',
                        'ignoreerrors': True,
                        'nowarnings': True,
                        'nooverwrites': True}

                with youtube_dl.YoutubeDL(opts) as ydl:
                    ydl.download([url])

            except ValueError:
                print("Couldn't download video: check your url or resolution of video, maybe it's too big")
        else:
            raise(ValueError, "Invalid resolution optinon: check documentation")
    else:
        raise(ValueError, "Wrong pornhub link: maybe this link is not a video link, but channel or playlist and etc.")
    
    if video_only:
        cmd = f"ffmpeg -i {video_path}output.mp4 -c:v copy -an {video_path + title}.mp4"
        os.system(cmd)
        return "Video download complete!"
    elif audio_only:
        cmd = f"ffmpeg -i {video_path}output.mp4 -c:a copy -vn {video_path + title}.mp4"
        os.system(cmd)
        return "Audio download complete!"
    else:
        os.rename(f"{video_path}output.mp4", f"{video_path + title}.mp4")
        return "Video and audio download complete!"

pornhub_info('https://rt.pornhub.com/view_video.php?viewkey=ph61b3097a3bcca')