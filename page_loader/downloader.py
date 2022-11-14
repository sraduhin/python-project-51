import requests
import os
import re
import logging
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from urllib.parse import urlparse

logging.basicConfig(filename='loader.log', level=logging.INFO)

VALID_IMG_EXTENSIONS = ['png', 'jpg']


def main(url, dir):
    logging.info('loader has been started')
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        logging.warning(f'HTTP error occurred: {http_err}')
    except Exception as err:
        logging.warning(f'Other error occurred: {err}')
    else:
        logging.info(f'success response. Status code: {response.status_code}')
        html_soup = BeautifulSoup(response.text, 'html.parser')
        host, local_name = get_host_and_create_local_name(url, dir)
        local_dir = local_name.replace('.html', '-files')
        os.makedirs(local_dir, exist_ok=True)
        origins = find_images(html_soup)
        logging.info(f'{len(origins)} images found. Downloading...')
        copies = []
        if origins:
            copies.extend(localize_src(origins, local_dir))
            for num, path in enumerate(origins):
                download_file(path, copies[num], images=True)
                logging.info(f'success!')
        origin_assets = find_links(html_soup, host)
        origin_assets.extend(find_scripts(html_soup))
        logging.info(f'{len(origin_assets)} assets found. Downloading...')
        if origin_assets:
            asset_copies = localize_src(origin_assets, local_dir)
            for num, path in enumerate(origin_assets):
                download_file(path, asset_copies[num])
                logging.info(f'success!')
        origins.extend(origin_assets)
        copies.extend(asset_copies)
        html = html_soup.prettify()
        for num, src in enumerate(origins):
            html = html.replace(src, copies[num])
        
        return download_html(html, local_name)


def get_host_and_create_local_name(url, dir=os.getcwd()):
    obj = urlparse(url)
    (name, ext) = os.path.splitext(obj.path)
    ext = ext or '.html'
    host = obj.hostname or ''
    name = os.path.join(dir, normalize(host + name)) + ext
    return host, name

# ----------- utils
def normalize(src):
    parts = re.split(r';|_|-|/|\.', src)
    return '-'.join(parts).strip('-')


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


def download_file(origin_path, copy_path, images=False):
    response = requests.get(origin_path)
    if images:
        with open(copy_path, 'wb') as copy:
            copy.write(response.content)
    else:
        with open(copy_path, 'w', encoding='utf-8') as copy:
            copy.write(response.text)


def download_html(html, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
        logging.info(f'html page has been successfully downloaded to {path}')
        return path


if __name__ == '__main__':
    main('https://ru.hexlet.io/courses', 'var\\tmp')