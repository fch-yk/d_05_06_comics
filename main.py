
import os
from pathlib import Path
from urllib.parse import unquote, urlsplit

import requests


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


def main():
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


if __name__ == '__main__':
    main()
