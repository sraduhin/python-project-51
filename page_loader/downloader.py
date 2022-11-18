import os
import logging

from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

from page_loader.utils import (
    download_file,
    download_html,
    find_assets,
    find_images,
    get_url,
    localize_src,
    parse_url,
)

logging.basicConfig(encoding='utf-8', level=logging.INFO)


def main(url, dir):
    logging.info(f'requested url: {url}')
    response = get_url(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    urls_component = parse_url(url)
    urls_component['name'] = os.path.join(
        dir, normalize(host + name)) + ext
    local_dir = urls_component['name'].replace('.html', '_files')
    html = html_soup.prettify()
    origins = find_images(html_soup)
    images_link_count = len(origins)
    origins.extend(find_assets(html_soup, urls_component['host']))
    if origins:
        os.makedirs(local_dir, exist_ok=True)
        copies = localize_src(origins, local_dir)
        progress = len(copies)
        with IncrementalBar('Processing', max=progress) as bar:
            for num, path in enumerate(origins):
                if num < images_link_count:
                    download_file(path, copies[num], urls_component, image=True)
                else:
                    download_file(path, copies[num], urls_component)
                html = html.replace(path, copies[num])
                bar.next()
    return download_html(html, urls_component['name'])


if __name__ == '__main__':
    main('https://ru.hexlet.io/3courses', 'var\\tmp')
