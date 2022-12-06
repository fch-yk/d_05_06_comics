
import os
import random
from contextlib import contextmanager
from dataclasses import dataclass
from urllib.parse import unquote, urlsplit

import requests
from environs import Env


@dataclass
class CommonVKSettings:
    access_token: str
    vk_api_version: str
    group_id: str


def get_link_extension(link):
    path = urlsplit(link).path
    unquoted_path = unquote(path)
    return os.path.splitext(unquoted_path)[1]


def download_image(url, file_path):
    response = requests.get(
        url,
        timeout=(3.05, 27)
    )
    response.raise_for_status()

    with open(file_path, 'wb') as file:
        file.write(response.content)


def get_max_comic_number():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url, timeout=(3.05, 27))
    response.raise_for_status()
    return response.json()['num']


def get_comic_card(comic_number):
    url = f'https://xkcd.com/{comic_number}/info.0.json'
    response = requests.get(url, timeout=(3.05, 27))
    response.raise_for_status()
    return response.json()


def get_upload_url(common_vk_settings: CommonVKSettings):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'access_token': common_vk_settings.access_token,
        'v': common_vk_settings.vk_api_version,
        'group_id': common_vk_settings.group_id,
    }
    response = requests.get(
        url,
        params=payload,
        timeout=(3.05, 27)
    )
    response.raise_for_status()
    return response.json()


def upload_photo(
    common_vk_settings: CommonVKSettings,
    upload_url: str,
    file_path: str
):
    payload = {
        'access_token': common_vk_settings.access_token,
        'v': common_vk_settings.vk_api_version,
        'group_id': common_vk_settings.group_id,
    }
    with open(file_path, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(
            upload_url,
            params=payload,
            files=files,
            timeout=(3.05, 27)
        )
    response.raise_for_status()

    return response.json()


def save_wall_photo(
    common_vk_settings: CommonVKSettings,
    photo: str,
    server: str,
    photo_hash: str,
):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'access_token': common_vk_settings.access_token,
        'v': common_vk_settings.vk_api_version,
        'group_id': common_vk_settings.group_id,
        'photo': photo,
        'server': server,
        'hash': photo_hash,
    }

    response = requests.post(
        url,
        params=payload,
        timeout=(3.05, 27)
    )
    response.raise_for_status()

    return response.json()


def post_photo(
    common_vk_settings: CommonVKSettings,
    owner_id,
    media_id,
    message
):
    url = 'https://api.vk.com/method/wall.post'
    payload = {
        'access_token': common_vk_settings.access_token,
        'v': common_vk_settings.vk_api_version,
        'owner_id': f'-{common_vk_settings.group_id}',
        'from_group': 1,
        'message': message,
        'attachments': f'photo{owner_id}_{media_id}',
    }

    response = requests.post(
        url,
        params=payload,
        timeout=(3.05, 27)
    )
    response.raise_for_status()


@contextmanager
def remove_tmp_file(file_path):
    try:
        yield
    finally:
        os.remove(file_path)


def main():
    env = Env()
    env.read_env()
    common_vk_settings = CommonVKSettings(
        env('VK_ACCESS_TOKEN'),
        '5.131',
        env('VK_GROUP_ID')
    )

    max_comic_number = get_max_comic_number()
    comic_number = random.randint(1, max_comic_number)
    comic_card = get_comic_card(comic_number)
    message = comic_card['alt']
    img_link = comic_card['img']
    extension = get_link_extension(img_link)
    file_path = f'comic_{comic_number}{extension}'
    download_image(img_link, file_path)

    with remove_tmp_file(file_path):
        upload_url_response = get_upload_url(common_vk_settings)
        if 'error' in upload_url_response:
            raise requests.ConnectionError(upload_url_response['error'])
        upload_url = upload_url_response['response']['upload_url']
        upload_response = upload_photo(common_vk_settings,
                                       upload_url,
                                       file_path
                                       )

    save_response = save_wall_photo(
        common_vk_settings,
        upload_response['photo'],
        upload_response['server'],
        upload_response['hash']

    )

    post_photo(
        common_vk_settings,
        save_response['response'][0]['owner_id'],
        save_response['response'][0]['id'],
        message
    )


if __name__ == '__main__':
    main()
