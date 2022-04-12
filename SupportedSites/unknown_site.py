import requests
from bs4 import BeautifulSoup
import random
import sys
from pathlib import Path


def unknown_site_check(url):
    return False

def unknown_site_get_docs():
    text ='''
+-------------------------+
| Unknown Sites:          |
+------+------------------+---------------------------+---------------------------------------------------------------+
|      |--info            |                           |  returns avaliable LINKS and indexes for video downloading    |
| url  |-p / -path        |  /full/path               |  by default locates downloads into (path to script)/downloads |
|      |-n / name         |  your_name                |  by default name generates with video title                   |
|      |-i / -index       |  1 / 2...                 |  by default index is None, returns Error with no given index  |
+------+------------------+---------------------------+---------------------------------------------------------------+
'''
    return text

def unknown_site_opt_func_check():
    return False

def unknown_site_idx_func_check():
    return True

def unknown_site_res_func_check():
    return False

def unknown_site_parser(url):
    formats = ['.3gp','.asf','.avi','.flv','.m2ts',
            '.m4v','.mkv','.mov','.mp4','.mts',
            '.ogg','.swf','.vob','.wmv','.rm']
    response = requests.get(url).text
    page = BeautifulSoup(response,'html.parser')
    links = []

    site_original_link = 'http://'
    for i in range(8, len(url)):
        if url[i] == '/':
            break
        else:
            site_original_link = site_original_link + url[i]
    
    href_links = []
    h_links = page.find_all('link')
    for link in h_links:
        try:
            href_links.append(link.__dict__['attrs']['href'])
        except:
            pass
    for link in href_links:
        links.append(link)
    
    source_links = []
    sources = page.find_all('source')
    for source in sources:
        try:
            source_links.append(source.__dict__['attrs']['src'])
        except:
            pass
    for s_link in source_links:
        links.append(site_original_link + s_link)

    vid_links = []
    for link in links:
        for form in formats:
            if form in link:
                vid_links.append(link)
                break
            elif not '.webmanifest' in link and '.webm' in link:
                vid_links.append(link)
                break

    return vid_links

def unknown_site_info(url):
    text = ' Avaliable link indexes:'
    parsed_page = unknown_site_parser(url)

    for i in range(len(parsed_page)):
        text = f'{text}\n   {i+1} - {parsed_page[i]}'

    return text 

def unknown_site_downloader(vid_links, opts, index, custom_name= None, custom_path= None):
    if len(vid_links) > 0:
        link = vid_links[index]
        response = requests.get(link)
        media = response.content

        if opts['index'] is None:
            print("ERROR: No given index for video file on the page, to get indexes use --info to your link")
            sys.exit()
        flag = False
        if opts['resolurion'] is not None:
            print("WARNING: -r (-resolution) option will be ignored")
            flag = True
        if opts['audio_only'] is not None or opts['video_only'] is not None:
            print("WARNING: -o (-option) option will be ignored")
            flag = True
        if flag:
            print("Use '--help unknown_site' too get more info")
        custom_path = opts['path']
        custom_name = opts['name']

        if custom_name is None:
            name = ""
            for i in range(10):
                name = name + str(random.randint(1, 100))
        else:
            name = custom_name
        
        if custom_path is None:
            path = f"{Path().resolve()}"
        else:
            path = custom_path
        open(f'{path}\{name}.mp4', 'wb').write(media)
    else:
        print("ERROR: No media links on this page")
