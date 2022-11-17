import requests
import os
import re
import sys
import logging
from urllib.parse import urlparse
from requests.exceptions import HTTPError

VALID_IMG_EXTENSIONS = ['png', 'jpg']

logging.basicConfig(encoding='utf-8', level=logging.INFO)


def get_host_and_create_local_name(url, dir=os.getcwd()):
    obj = urlparse(url)
    (name, ext) = os.path.splitext(obj.path)
    ext = ext or '.html'
    host = obj.hostname or ''
    name = os.path.join(dir, normalize(host + name)) + ext
    return host, name


def get_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def normalize(src):
    parts = re.split(r';|_|-|/|\.', src)
    return '-'.join(parts).strip('-.').replace('--', '-')


def find_images(html):
    images = []
    for link in html.find_all('img'):
        src = link.get('src')
        (_, extension) = os.path.splitext(src)
        if extension[1:] in VALID_IMG_EXTENSIONS:
            images.append(src)
    return images


def find_links(html, localhost):
    links = []
    for tagline in html.find_all('link'):
        href = tagline.get('href')
        originhost = urlparse(href).hostname
        if not originhost or originhost == localhost:
            links.append(href)
    return links


def find_scripts(html):
    scripts = []
    for tagline in html.find_all('script'):
        src = tagline.get('src')
        if src:
            scripts.append(src)
    return scripts


def localize_src(list, dir):
    locals = []
    for element in list:
        _, name = get_host_and_create_local_name(element, dir)
        locals.append(name)
    return locals


def download_file(origin_path, copy_path, image=False):
    response = get_url(origin_path)
    if image:
        with open(copy_path, 'wb') as copy:
            copy.write(response.content)
    else:
        with open(copy_path, 'w', encoding='utf-8') as copy:
            copy.write(response.text)
    logging.debug(f'success download to {copy_path}')


def download_html(html, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
        logging.info(f'html page has been successfully downloaded to {path}')
        return path
