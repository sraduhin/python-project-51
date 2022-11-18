import requests
import os
import re
import logging
from urllib.parse import urlparse

VALID_IMG_EXTENSIONS = ['png', 'jpg']

logging.basicConfig(encoding='utf-8', level=logging.INFO)


def get_host_and_create_local_name(url, dir=os.getcwd()):
    obj = urlparse(url)
    (name, ext) = os.path.splitext(obj.path)
    ext = ext or '.html'
    host = obj.hostname or ''
    name = os.path.join(dir, normalize(host + name)) + ext
    return host, scheme, name


def parse_url(url, dir=os.getcwd()):
    data = {}
    obj = urlparse(url)
    name, ext = os.path.splitext(obj.path)
    data['extension'] = ext or '.html'
    data['name'] = os.path.join(dir, normalize(host + name)) + ext
    if obj.hostname:
        data['host'] = obj.hostname
    if obj.scheme:
        data['scheme'] = obj.scheme
    return data


def localize_src(list, dir):
    locals = []
    for element in list:
        _, name = get_host_and_create_local_name(element, dir)
        locals.append(name)
    return locals


def normalize(src):
    parts = re.split(r';|_|-|/|\.', src)
    return '-'.join(parts).strip('-.').replace('--', '-')


def get_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def find_images(html):
    images = []
    for link in html.find_all('img'):
        src = link.get('src')
        (_, extension) = os.path.splitext(src)
        if extension[1:] in VALID_IMG_EXTENSIONS:
            images.append(src)
    return images


def find_assets(html, localhost=None):
    assets = []
    assets_links = html.find_all(['script', 'link'])
    for link in assets_links:
        href = link.get('href')
        if localhost and href:
            originhost = urlparse(href).hostname
            if originhost and originhost != localhost:
                continue
            assets.append(href)
        src = link.get('src')
        if src:
            assets.append(src)
    return assets


def download_file(origin_path, copy_path, image=False, host=False, scheme):
    print('>>>', host)
    if host:
        origin_path = host + origin_path
    print('>>>', origin_path)
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
