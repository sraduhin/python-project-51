import logging

from bs4 import BeautifulSoup

from page_loader.utils import parse_url

VALID_IMG_EXTENSIONS = ['.png', '.jpg']


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


def get_locals(content):
    content = BeautifulSoup(content, 'html.parser')
    images = list(
        filter(
            lambda x: parse_url(x)['extension'] in VALID_IMG_EXTENSIONS,
            [row.get('src') for row in content.find_all('img')]
        )
    )


    local_page_name = create_local_name(url)
    local_dir = local_page_name.replace('.html', '_files')

    images = find_images(html)
    assets = find_assets(html, parent=url)
    resourses = images + assets
    # html = html.prettify(formatter=HTMLFormatter(indent=4))
    html = html.prettify()