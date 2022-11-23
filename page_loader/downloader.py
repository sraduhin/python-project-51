import os
import logging


from bs4 import BeautifulSoup
# from bs4.formatter import HTMLFormatter
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

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


def main(url, dir, downloader=download_file):
    logging.info(f'requested url: {url}')

    if not os.path.isdir(dir):
        raise FileNotFoundError(f'{dir} doesnt exist')

    response = get_html(url)
    html = BeautifulSoup(response.text, 'html.parser')

    local_page_name = create_local_name(url)
    local_dir = local_page_name.replace('.html', '_files')

    images = find_images(html)
    assets = find_assets(html, parent=url)
    resourses = images + assets
    # html = html.prettify(formatter=HTMLFormatter(indent=4))
    html = html.prettify()

    if resourses:
        os.makedirs(os.path.join(dir, local_dir), exist_ok=True)

        with IncrementalBar('Processing', max=len(resourses)) as bar:
            for path in resourses:
                full_origin_path = normalize_link(path, parent=url)
                local_file_name = create_local_name(full_origin_path)
                relative_local_path = os.path.join(local_dir, local_file_name)
                absolut_local_path = os.path.join(dir, relative_local_path)
                downloader(full_origin_path, absolut_local_path)
                # download_file(full_origin_path, absolut_local_path)
                html = html.replace(path, relative_local_path)
                logging.debug(
                    f"{path} saved with new local name {local_file_name}"
                )
                bar.next()

    absolut_page_path = os.path.join(dir, local_page_name)
    download_html(html, absolut_page_path)
    return absolut_page_path
