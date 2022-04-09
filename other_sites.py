import requests
from bs4 import BeautifulSoup
import random
from pathlib import Path

def site_parser(url):
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

def site_info(url):
    text = ' Avaliable link indexes:'
    parsed_page = site_parser(url)

    for i in range(len(parsed_page)):
        text = f'{text}\n   {i+1} - {parsed_page[i]}'

    return text 

def site_downloader(vid_links, index, custom_name= None, custom_path= None):
    if len(vid_links) > 0:
        link = vid_links[index]
        response = requests.get(link)
        media = response.content

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
        open(f'{path}{name}.mp4', 'wb').write(media)
    else:
        raise(ValueError, "No media links on this page")
