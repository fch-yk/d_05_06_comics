
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
    connect_timeout = 3.05
    read_timeout = 27
    response = requests.get(
        url,
        params=payload,
        timeout=(connect_timeout, read_timeout)
    )
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


def get_upload_url(access_token, vk_api_version, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'access_token': access_token,
        'v': vk_api_version,
        'group_id': group_id,
    }
    connect_timeout = 3.05
    read_timeout = 27
    response = requests.get(
        url,
        params=payload,
        timeout=(connect_timeout, read_timeout)
    )
    response.raise_for_status()
    return response.json()['response']['upload_url']


def upload_photo(
    access_token,
    vk_api_version,
    group_id,
    upload_url,
    file_path
):
    payload = {
        'access_token': access_token,
        'v': vk_api_version,
        'group_id': group_id,
    }
    with open(file_path, 'rb') as file:
        files = {
            'photo': file,
        }
        connect_timeout = 3.05
        read_timeout = 27
        response = requests.post(
            upload_url,
            params=payload,
            files=files,
            timeout=(connect_timeout, read_timeout)
        )
        response.raise_for_status()

    return response.json()


def save_wall_photo(
    access_token,
    vk_api_version,
    group_id,
    upload_response,
    caption
):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'access_token': access_token,
        'v': vk_api_version,
        'group_id': group_id,
        'photo': upload_response['photo'],
        'server': upload_response['server'],
        'hash': upload_response['hash'],
        'caption': caption,
    }

    connect_timeout = 3.05
    read_timeout = 27
    response = requests.post(
        url,
        params=payload,
        timeout=(connect_timeout, read_timeout)
    )
    response.raise_for_status()

    return response.json()


def main():
    env = Env()
    env.read_env()
    access_token = env('ACCESS_TOKEN')
    vk_api_version = 5.131
    group_id = env('GROUP_ID')
    # get_comic()
    # get_groups(access_token, vk_api_version)
    upload_url = get_upload_url(access_token, vk_api_version, group_id)
    file_path = './images/comic_353.png'
    upload_response = upload_photo(
        access_token,
        vk_api_version,
        group_id,
        upload_url,
        file_path,
    )
    caption = 'comic about python'
    save_response = save_wall_photo(
        access_token,
        vk_api_version,
        group_id,
        upload_response,
        caption
    )

    pprint.pprint(save_response)


if __name__ == '__main__':
    main()
