import re
import os
import logging

from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

from page_loader.urls import create_local_name, get_url_content
from page_loader.urls import get_url, parse_url

logging.basicConfig(encoding='utf-8', level=logging.INFO)

VALID_IMG_EXTENSIONS = ['.png', '.jpg']


def get_content_and_assets(url):
    content = get_url_content(url)
    content = BeautifulSoup(content, 'html.parser')
    assets = []

    # find <img>
    pattern = f".+?.({'|'.join(VALID_IMG_EXTENSIONS)})$"
    tags = content.find_all('img', src=re.compile(pattern))

    # find <script>
    # pattern: no host or parent's host
    pattern = f"(^/)|:(//{parse_url(url)['host']})"
    tags.extend(content.find_all('script', src=re.compile(pattern)))

    # find <link> by same pattern
    tags.extend(content.find_all('link', href=re.compile(pattern)))
    pathes = [x.get('src') or x.get('href') for x in tags]

    content = content.prettify()

    assets_directory = create_local_name(url).replace('.html', '_files')

    for path in pathes:
        url_path = get_url(path, url)
        local_path = os.path.join(
            assets_directory, create_local_name(url_path)
        )
        content = content.replace(path, local_path)
        assets.append((url_path, local_path))

    return content, assets


def download_assets(assets, dir=None):

    with IncrementalBar('Processing', max=len(assets)) as bar:

        for url, local in assets:
            logging.debug(f'downloading {url}')
            local_path = os.path.join(dir or '', local)
            content = get_url_content(url)

            with open(local_path, 'wb') as copy:
                copy.write(content)

            bar.next()
