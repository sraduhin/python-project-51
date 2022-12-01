import os
import logging

from page_loader.urls import create_local_name
from page_loader.assets import get_content_and_assets, download_assets

logging.basicConfig(encoding='utf-8', level=logging.INFO)


def download(url, dir, downloader=download_assets):
    logging.info(f'requested url: {url}')

    if not os.path.isdir(dir):
        raise FileNotFoundError(f'{dir} doesnt exist')

    html, assets = get_content_and_assets(url)
    local_page_name = create_local_name(url)

    if assets:
        assets_directory = local_page_name.replace('.html', '_files')
        os.makedirs(os.path.join(dir, assets_directory), exist_ok=True)
        downloader(assets, dir)

    path = os.path.join(dir, local_page_name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
        logging.info(f'html page has been successfully downloaded to {path}')

    return path
