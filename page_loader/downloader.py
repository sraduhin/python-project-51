import requests
import os
import re
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from urllib.parse import urlparse

VALID_IMG_EXTENSIONS = ['png', 'jpg']


def main(url, dir):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        html_soup = BeautifulSoup(response.text, 'html.parser')
        host, local_name = parse_url(url, dir)
        local_dir = local_name.replace('.html', '-files')
        os.makedirs(local_dir, exist_ok=True)
        origin_images = find_images(html_soup)
        if origin_images:
            copies = localize_src(origin_images, local_dir)
            download_images(origin_images, copies)
            html = html_soup.prettify()
            for num, src in enumerate(origin_images):
                html = html.replace(src, copies[num])
        origin_assets = 
        return download_html(html, local_name)


def parse_url(url, dir=os.getcwd()):
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
    for link in html.find_all('link', 'script'):
        src = link.get('src')
        (_, extension) = os.path.splitext(src)
        if extension[1:] in VALID_IMG_EXTENSIONS:
            images.append(src)
    return images


def find_assets(html):
    assets = []
    for link in html.find_all('s'):
        src = link.get('src')
        (_, extension) = os.path.splitext(src)
        if extension[1:] in VALID_IMG_EXTENSIONS:
            images.append(src)
    return images


def localize_src(list, dir):
    locals = []
    for element in list:
        _, name = parse_url(element, dir)
        locals.append(name)
    return locals


def download_images(origins, locals):
    for num, path in enumerate(locals):
        image = requests.get(origins[num])
        with open(path, 'wb') as copy:
            copy.write(image.content)


def download_html(html, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
        return path


if __name__ == '__main__':
    main('https://ru.hexlet.io/courses', 'var\\tmp')