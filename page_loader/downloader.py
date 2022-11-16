import os
import requests
import logging

from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

from page_loader.utils import get_host_and_create_local_name, localize_src, download_file, download_html, find_images, find_links, find_scripts

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

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
        origins.extend(origin_assets)
        copies.extend(asset_copies)
        html = html_soup.prettify()
        for num, src in enumerate(origins):
            html = html.replace(src, copies[num])
        return download_html(html, local_name)


if __name__ == '__main__':
    main('https://ru.hexlet.io/3courses', 'var\\tmp')