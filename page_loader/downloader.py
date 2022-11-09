import requests
import os
import re
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

VALID_EXTENSIONS = ['png', 'jpg']


def get_file_name(url):
    host = url.split('//')[-1]
    return re.sub(r'[./]', '-', host) + '.html'


def parse_http(url, dir):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Success!')
        return response.text
'''
def download(url, dir):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        file_name = get_file_name(url)
        os.makedirs(dir, exist_ok=True)
        download_path = os.path.join(dir, file_name)
        with open(download_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
            print('Success!')
            return download_path'''

def parse_img_tag(html_doc):
    print(html_doc)
    soup = BeautifulSoup(html_doc, 'html.parser')
    img_links = []
    for link in soup.find_all('img'):
        img_links.append(link.get('src'))
    print(filter(img_links, ))
    

def download_html(html, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
        print('Success!')
        return path

def safe_pictures(pathfile):
    with open(pathfile, 'r', encoding='utf-8') as html_doc:
        html_doc = html_doc.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        



if __name__ == '__main__':
    html = parse_http('https://ru.hexlet.io/courses', 'var\\tmp')
    parse_img_tag(html)
    # safe_pictures('var\\tmp\\ru-hexlet-io-courses.html')