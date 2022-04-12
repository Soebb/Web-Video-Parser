from pathlib import Path
import requests
import os
from bs4 import BeautifulSoup
import time
from selenium import webdriver


def newgrounds_check(url):
    if 'newgrounds.com' in url:
        return True
    return False

def newgrounds_opt_func_check():
    return True

def newgrounds_idx_func_check():
    return False

def newgrounds_res_func_check():
    return True

def newgrounds_get_docs():
    text = '''
+-------------------------+
| Newgrounds:             |
+------+------------------+---------------------------+---------------------------------------------------------------+
|      |--info            |                           |  returns avaliable resolutions for video downloading          |
|      |-o / -option      |  video_only / audio_only  |  by dafault downloads video and audio                         |
| url  |-p / -path        |  /full/path               |  by default locates downloads into (path to script)/downloads |
|      |-n / name         |  your_name                |  by default name generates with video title                   |
|      |-r / -resolution  |  144 / 240/ ... / 2160..  |  by default resolution is highest                             |
+------+------------------+---------------------------+---------------------------------------------------------------+
'''
    return text

def newgrounds_parser(url):
    driver = webdriver.Firefox()
    driver.minimize_window()
    driver.get(url)

    button = driver.find_element_by_xpath('/html/body/div[10]/div[3]/div/div[2]/div/div[2]')
    button.click()
    time.sleep(0.1)
    stop_button = driver.find_element_by_xpath('/html/body/div[10]/div[3]/div/div')
    stop_button.click()

    page = driver.page_source
    page = BeautifulSoup(page, 'html.parser')
    driver.close()
    title = page.find('h2', {'itemprop': 'name'}).contents[0]
    links = []
    link = page.find('source', type = "video/mp4").attrs['src']
    clear_link = ''

    flag = False
    res_position = None
    len_sliced = 2

    for i in range(1, len(link)+1):
        if link[-i] != '.' and not flag:
            clear_link = link[-i] + clear_link
        elif link[-i] == '.' and not flag:
            clear_link = link[-i] + clear_link
            flag = True
        elif link[-i] != '.' and flag:
            len_sliced += 1
        elif link[-i] == '.' and flag:
            clear_link = link[0:-i] + clear_link
            res_position = -i-1
            break

    res_info = page.find_all('div', {'data-options': 'res'})[0].__dict__['contents']
    resolutions = []
    for res_inf in res_info:
        resolutions.append(res_inf.attrs['data-value'][:-1])
    for res in resolutions:
        links.append(clear_link[0:(res_position + len_sliced)] + '.' + res + 'p' + clear_link[(res_position + len_sliced):])
    get_by_res = {}
    for i in range(len(links)):
        get_by_res[resolutions[i]] = links[i]
    return resolutions, links, get_by_res, title

def newgrounds_info(url):
    if "https://www.newgrounds.com/portal/view/" in url:
        parsed_page = newgrounds_parser(url)
        text = f"Newgrounds video title: {parsed_page[3]}\nAvaliable resolutions:\n  "
        for res in parsed_page[0]:
            text = text + f"{res}p, "
        text = text[:-2]
        return text
    else:
        print("ERROR: It's not a video link, maybe something else...")

def newgrounds_downloader(url, opts):
    if "https://www.newgrounds.com/portal/view/" in url:
        if opts['index'] is not None:
            print("WARNING: -i (-index) option will be ignored, use '--help newgrounds' too get more info")

        resolution = opts['resolution']
        video_only = opts['video_only']
        audio_only = opts['audio_only']
        custom_path = opts['path']
        custom_name = opts['name']

        parsed_page = newgrounds_parser(url)

        if resolution == 'best':
            url = parsed_page[2][parsed_page[0][0]]
        else:
            url = parsed_page[2][resolution]

        response = requests.get(url).content

        if custom_name is None:
            name = parsed_page[3]
            name.replace(' ', '_')
        else:
            name = custom_name

        if custom_path is None:
            path = Path().resolve()
        else:
            path = custom_path

        out_path = f'{path}\output.mp4'
        open(out_path,'wb').write(response)

        if video_only:
            cmd = f"ffmpeg -i {path}\output.mp4 -c:v copy -an {path}\{name}.mp4"
            os.system(cmd)
            os.remove(f'{path}\output.mp4')
        elif audio_only:
            cmd = f"ffmpeg -i {path}\output.mp4 -a:v copy -vn {path}\{name}.mp4"
            os.system(cmd)
            os.remove(f'{path}\output.mp4')
        else:
            os.rename(f'{path}\output.mp4', f"{name}.mp4")

        return "Downloading complete!"
    else:
        print("ERROR: It's not a video link, maybe something else...")