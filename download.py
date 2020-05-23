
import os
import json
import requests
from pathlib import Path
from urllib.parse import urlparse
from requests_oauthlib import OAuth1

api_key = "34e8456a2c744d52bed996d9156adedb"
api_secret = "25d3c8e106f94aa3a1f87300bca0ec5e"
endpoint_url = "http://api.thenounproject.com/icons/{}?limit={}&offset={}"
icon_folder = "./icons/{}/{}/"
download_limit = 50
start_no = 1
end_no = start_no + 50000

termslist = [
    "Flowers",
    "Circle",
    "Crown",
    "House",
    "Girl",
    "Clothes",
    "Abstract",
    "Heart",
    "Sport",
    "Square",
    "Tree",
    "Triangle"
]

def download_icon(id, term, url):
    global icon_folder
    media_path = urlparse(url).path
    path_arr = os.path.split(media_path)
    media_filename = path_arr[len(path_arr)-1]
    media_filefolder = icon_folder.format(term, id)
    media_filepath = media_filefolder + media_filename    
    try:
        if not os.path.exists(media_filefolder):
            os.makedirs(media_filefolder)
    except FileExistsError:
        pass

    try:
        res = requests.get(url, allow_redirects=True)
        open(media_filepath, "wb").write(res.content)
    except:
        pass    

if __name__ == '__main__':    
    auth = OAuth1(api_key, api_secret)

    for term in termslist:
        print("-:", term)
        offset = start_no
        while True:
            endpoint = endpoint_url.format(term, download_limit, offset)
            print(endpoint)
            response = requests.get(endpoint, auth=auth)
            json_content = response.text
            json_obj = json.loads(json_content)
            icons_obj = json_obj['icons']
            for icon_node in icons_obj:
                icon_id = icon_node['id']
                if 'attribution_preview_url' in icon_node:
                    attribution_preview_url = icon_node['attribution_preview_url']
                    print("--:", icon_id, attribution_preview_url)
                    download_icon(icon_id, term, attribution_preview_url)
                if 'preview_url' in icon_node:
                    preview_url = icon_node['preview_url']
                    print("--:", icon_id, preview_url)
                    download_icon(icon_id, term, preview_url)
                if 'preview_url_42' in icon_node:
                    preview_url_42 = icon_node['preview_url_42']
                    print("--:", icon_id, preview_url_42)
                    download_icon(icon_id, term, preview_url_42)
                if 'preview_url_84' in icon_node:
                    preview_url_84 = icon_node['preview_url_84']
                    print("--:", icon_id, preview_url_84)
                    download_icon(icon_id, term, preview_url_84)
                
            offset = offset + download_limit
            if offset >= end_no:
                break


