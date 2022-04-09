import sys
import requests
from youtube import *
from pornhub import *
from other_sites import *


def url_check(url):
    try:
        requests.get(str(url))
        requests.delete(str(url))
        return True
    except ValueError:
        print("This url is invalid")

def get_url_type(url):
    if 'youtube' in url or 'youtu.be' in url:
        return 'youtube'
    if 'pornhub' in url:
        return 'pornhub'
    else:
        return 'unknown'        

def docs(request):
    return request

def info_loader(url):
    if get_url_type(url) == 'youtube':
        return youtube_info(url)
    elif get_url_type(url) == 'pornhub':
        return pornhub_info(url)
    else:
        return site_info(url)

def download(url, opts):
    if url_check(url):
        url_type = get_url_type(url)
        if url_type == 'youtube':
            parsed_ytpage = youtube_parser(url)
            res_list = parsed_ytpage[0]
            res_tags = parsed_ytpage[1]
            audio_itag = parsed_ytpage[3]
            if opts['resolution'] == "best":
                return youtube_downloader(url, res_list[-1], res_tags, audio_tag = audio_itag,
                                        audio_only = opts['audio_only'], video_only = opts['video_only'],
                                        custom_name = opts['name'], custom_path = opts['path'])
            else:
                return youtube_downloader(url, opts['resolution'], res_tags, audio_tag = audio_itag,
                                        audio_only = opts['audio_only'], video_only = opts['video_only'],
                                        custom_name = opts['name'], custom_path = opts['path'])
        elif url_type == 'pornhub':
            if opts['resolution'] == "best":
                resolutions = ['2160','1440','1080','720','480','360','240']
                video_ress = get_resolutions(url)
                for res in resolutions:
                    if res in video_ress:
                        resolution = res
                        break
                return pornhub_downloader(url, resolution, audio_only = opts['audio_only'],
                                        video_only = opts['video_only'], custom_name = opts['name'],
                                        custom_path = opts['path'])
        else:
            if opts['index'] is not None:
                return site_downloader(site_parser(url), int(opts['index'])-1, custom_name = opts['name'], custom_path = opts['path'])
            else:
                raise(ValueError, "You didn't type the index of video file, to know indexes use --info on your link")

def main():
    cmd = sys.argv

    if len(cmd) > 1:

        if cmd[1] == '--help':
            if len(cmd) > 1:
                if cmd[1] == 'youtube':
                    return docs('youtube')
                if cmd[1] == 'pornhub':
                    return docs('pornhub')
                if cmd[1] == 'other':
                    return docs('other')
            else:
                return docs('all')
        
        elif url_check(cmd[1]):
            opts = {'video_only': False,
                    'audio_only': False,
                    'resolution': "best",
                    'name': None,
                    'path': None,
                    'index': None}
            ignore_element = False
            option_flag = False
            resolution_flag = False
            name_flag = False
            path_flag = False
            index_flag = False

            if len(cmd) > 2:
                url_type = get_url_type(cmd[1])

                for i in range(2, len(cmd)):

                    if ignore_element:
                        ignore_element = False
                        pass

                    elif cmd[i] == '--info':
                        if len(cmd) > 3:
                            print("Warning: arguments after --info won't be used")
                        print(info_loader(cmd[1]))
                        sys.exit()

                    elif cmd[i] == '-o' or cmd[i] == '-option':
                        if option_flag:
                            print("Warning: other -o (-option) commands will be ignored")
                        elif url_type == 'unknown':
                            raise(ValueError, "-o (-optinon) command can't be used for Unknown type url")

                        elif len(cmd) > i+1:
                            if cmd[i+1] == 'video_only':
                                opts['video_only'] = True
                            elif cmd[i+1] == 'audio_only':
                                opts['audio_only'] = True
                            else:
                                raise(ValueError, f"-o (-option) command don't have {cmd[i]} argument")
                            option_flag = True
                            ignore_element = True
                        
                        else:
                            raise(ValueError, "No arguments after -o (-option) command")

                    elif cmd[i] == '-r' or cmd[i] == '-resolution':
                        if resolution_flag:
                            print("Warning: other -r (-resolution) commands will be ignored")
                        elif url_type == 'unknown':
                            raise(ValueError, "Can't get video by custom resolution from Unknown type url")

                        elif len(cmd) > i+1:
                            opts['resolution'] = cmd[i+1]
                            resolution_flag = True
                            ignore_element = True

                        else:
                            raise(ValueError, "No arguments after -r (-resolution) command")
                    
                    elif cmd[i] == '-n' or cmd[i] == '-name':
                        if name_flag:
                            print("Warning: other -n (-name) commands will be ignored")

                        elif len(cmd) > i+1:
                            opts['name'] = cmd[i+1]
                            name_flag = True
                            ignore_element = True

                        else:
                            raise(ValueError, "No arguments after -n (-name) command")
                    
                    elif cmd[i] == '-p' or cmd[i] == '-path':
                        if path_flag:
                            print("Warning: other -p (-path) commands will be ignored")

                        elif len(cmd) > i+1:
                            opts['path'] = cmd[i+1]
                            path_flag = True
                            ignore_element = True

                        else:
                            raise(ValueError, "No arguments after -p (-path) command")
                    
                    elif cmd[i] == '-i' or cmd[i] == '-index':
                        if index_flag:
                            print("Warning: other -i (-index) commands will be ignored")
                        elif url_type != 'unknown':
                            raise(ValueError, "You can get the video by index only for unknown type urls")

                        elif len(cmd) > i+1:
                            opts['index'] = cmd[i+1]
                            index_flag = True
                            ignore_element = True

                        else:
                            raise(ValueError, "No arguments after -i (-index) command")

                    else:
                        raise(ValueError, f"No command named {cmd[i]}")
                
            return download(cmd[1], opts)

    else:
        raise(ValueError, "No arguments got")

if __name__ == '__main__':
    main()