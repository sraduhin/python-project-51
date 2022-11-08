import requests
import os
import re
from requests.exceptions import HTTPError


def get_file_name(url):
    host = url.split('//')[-1]
    return re.sub(r'[./]', '-', host) + '.html'

def download(url, dir):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Success!')
        file_name = get_file_name(url)
        os.makedirs(dir, exist_ok=True)
        download_path = os.path.join(dir, file_name)
        with open(download_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
            print(download_path)


if __name__ == '__main__':
    download('https://ru.hexlet.io/courses', 'var\\tmp')