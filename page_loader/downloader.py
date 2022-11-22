import os
import logging

from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

from page_loader.utils import (
    create_local_name,
    download_file,
    download_html,
    find_images,
    find_assets,
    get_html,
    normalize_link,
)

logging.basicConfig(encoding='utf-8', level=logging.INFO)


def main(url, dir):
    logging.info(f'requested url: {url}')
    response = get_html(url)
    html = BeautifulSoup(response.text, 'html.parser')
    local_page_name = create_local_name(url)
    local_dir = local_page_name.replace('.html', '_files')
    images = find_images(html)
    assets = find_assets(html, parent=url)
    resourses = images + assets
    html = html.prettify()
    if resourses:
        os.makedirs(os.path.join(dir, local_dir), exist_ok=True)
        with IncrementalBar('Processing', max=len(resourses)) as bar:
            for num, path in enumerate(resourses):
                full_origin_path = normalize_link(path, parent=url)
                local_file_name = create_local_name(full_origin_path)
                relative_local_path = os.path.join(local_dir, local_file_name)
                image_type = [True, False][num < len(images)]
                absolut_local_path = os.path.join(dir, relative_local_path)
                download_file(full_origin_path, absolut_local_path, image_type)
                html = html.replace(path, relative_local_path)
                logging.debug(
                    f"{path} saved with new local name {local_file_name}"
                )
                bar.next()

    absolut_page_path = os.path.join(dir, local_page_name)
    download_html(html, absolut_page_path)
    return absolut_page_path
