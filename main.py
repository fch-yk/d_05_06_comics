
import os
import pprint
from pathlib import Path
from urllib.parse import unquote, urlsplit

import requests
from environs import Env


def get_link_extension(link):
    path = urlsplit(link).path
    unquoted_path = unquote(path)
    return os.path.splitext(unquoted_path)[1]


def download_image(url, folder_name, file_name, payload=None):
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(folder_name, file_name)

    response = requests.get(url, params=payload)
    response.raise_for_status()

    with open(file_path, 'wb') as file:
        file.write(response.content)


def get_comic():
    comic_number = 353
    url = f'https://xkcd.com/{comic_number}/info.0.json'
    connect_timeout = 3.05
    read_timeout = 27
    response = requests.get(url, timeout=(connect_timeout, read_timeout))
    response.raise_for_status()
    folder_name = 'images'
    comic_card = response.json()
    img_link = comic_card['img']
    extension = get_link_extension(img_link)
    download_image(img_link, folder_name, f'comic_{comic_number}{extension}')
    comment = comic_card['alt']
    print(comment)


def get_groups(access_token, vk_api_version):
    url = 'https://api.vk.com/method/groups.get'
    payload = {
        'access_token': access_token,
        'v': vk_api_version,
        'extended': 1,
    }
    connect_timeout = 3.05
    read_timeout = 27
    response = requests.get(
        url,
        params=payload,
        timeout=(connect_timeout, read_timeout)
    )
    response.raise_for_status()
    groups = response.json()
    pprint.pprint(groups)


def main():

    env = Env()
    env.read_env()
    access_token = env('ACCESS_TOKEN')
    # get_comic()
    vk_api_version = 5.131
    get_groups(access_token, vk_api_version)


if __name__ == '__main__':
    main()
