import os
import logging

from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

from page_loader.utils import (
    create_local_name,
    download_file,
    download_html,
    find_images,
    find_links,
    find_scripts,
    get_html,
    normalize_link,
)

logging.basicConfig(encoding='utf-8', level=logging.INFO)


def main(url, dir):
    logging.info(f'requested url: {url}')
    response = get_html(url)
    html = BeautifulSoup(response.text, 'html.parser')
    print(html.prettify())  # delete
    local_name = create_local_name(url, dir)
    local_dir = local_name.replace('.html', '_files')
    images = find_images(html)
    links = find_links(html, parent=url)
    scripts = find_scripts(html, parent=url)
    resourses = images + links + scripts
    html = html.prettify()
    if resourses:
        os.makedirs(local_dir, exist_ok=True)
        with IncrementalBar('Processing', max=len(resourses)) as bar:
            for num, path in enumerate(resourses):
                path = normalize_link(path, parent=url)
                local_file_name = create_local_name(path, local_dir, parent=url)
                if num < len(images):
                    download_file(path, local_file_name, image=True)
                else:
                    download_file(path, local_file_name)
                html = html.replace(path, local_file_name)
                logging.debug(f"{path} saved with new local name {local_file_name}")
                bar.next()
    download_html(html, local_name)
    return local_name
