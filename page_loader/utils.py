import requests
import os
import re
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse

VALID_IMG_EXTENSIONS = ['.png', '.jpg']

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


def parse_url(url):
    parts = {}
    obj = urlparse(url)
    parts['host'] = obj.hostname
    parts['scheme'] = obj.scheme
    parts['path'] = obj.path
    parts['name'], parts['extension'] = os.path.splitext(parts['path'])
    return parts


def create_local_name(url):
    url_parts = parse_url(url)
    extension = url_parts['extension'] or '.html'
    host = url_parts['host']
    name = normalize(host + url_parts['name'])
    name += extension
    return name


def normalize_link(link, parent):
    link_obj = parse_url(link)
    if not link_obj['scheme']:
        parents = parse_url(parent)
        link = f"{parents['scheme']}://{parents['host']}{link}"
    return link


def normalize(src):
    parts = re.split(r';|_|-|/|\.', src)
    return '-'.join(parts).strip('-.').replace('--', '-')


def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def find_images(html):
    images = []
    for link in html.find_all('img'):
        src = link.get('src')
        if src:
            src_parts = parse_url(src)
            if src_parts['extension'] in VALID_IMG_EXTENSIONS:
                logging.debug(f'found image {src}')
                images.append(src)
    return images


def find_assets(html, parent):
    assets = []
    for link in html.find_all(['script', 'link']):
        src = link.get('src') or link.get('href')
        if src:
            src_parts = parse_url(src)
            if src_parts['host']:
                parents = parse_url(parent)
                if src_parts['host'] == parents['host']:
                    logging.debug(f'found link {src}')
                    assets.append(src)
                continue
            assets.append(src)
    return assets


def download_file(origin_path, download_path, image=False):
    logging.debug(f'downloading {origin_path}')
    response = get_html(origin_path)
    if image:
        with open(download_path, 'wb') as copy:
            copy.write(response.content)
    else:
        with open(download_path, 'w') as copy:
            content = response.text
            content = BeautifulSoup(content, 'html.parser')
            copy.write(content.prettify())
    logging.debug(f'success download to {download_path}')


def download_html(html, path):
    logging.debug(f'downloading html page to {path}')
    with open(path, 'w') as f:
        f.write(html)
        logging.info(f'html page has been successfully downloaded to {path}')
