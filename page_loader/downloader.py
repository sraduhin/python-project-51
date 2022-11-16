import os
import logging

from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

from page_loader.utils import (
    download_file,
    download_html,
    find_images,
    find_links,
    find_scripts,
    get_host_and_create_local_name,
    get_url,
    localize_src,
)

logging.basicConfig(encoding='utf-8', level=logging.INFO)


def main(url, dir):
    logging.info(f'requested url: {url}')
    response = get_url(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    host, local_name = get_host_and_create_local_name(url, dir)
    local_dir = local_name.replace('.html', '-files')
    html = html_soup.prettify()
    origins = find_images(html_soup)
    images_link_count = len(origins)
    origins.extend(find_links(html_soup, host))
    origins.extend(find_scripts(html_soup))
    if origins:
        os.makedirs(local_dir, exist_ok=True)
        copies = localize_src(origins, local_dir)
        progress = len(copies)
        with IncrementalBar('Processing', max=progress) as bar:
            for num, path in enumerate(origins):
                if num < images_link_count:
                    download_file(path, copies[num], image=True)
                else:
                    download_file(path, copies[num])
                html = html.replace(path, copies[num])
                bar.next()
    return download_html(html, local_name)


if __name__ == '__main__':
    main('https://ru.hexlet.io/3courses', 'var\\tmp')
