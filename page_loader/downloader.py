import requests
import os
import re
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

VALID_EXTENSIONS = ['png', 'jpg']


def main(url, dir):
    html_doc, name = parse_http(url)
    #local_path = os.path.join(dir, name)
    #local_pathfiles = local_path + '-files'
    os.makedirs(local_pathfiles, exist_ok=True)
    html_doc = save_pics(html_doc, local_pathfiles)
    local_pagepath = local_path + '.html'
    download_html(html_doc, local_pagepath)
    return local_path


# ----------- utils
def get_file_name(src):
    filename = re.sub(r'(http[s]*?\://www.|http[s]*?\://|^www.)', '', src)
    filename = re.sub(r'[./]', '-', filename)    
    return re.sub(r'-$', '', filename)    
#------------


def parse_http(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        page_name = get_file_name(url)
        return response.text, page_name

def check_tags(tag, condition):
    def wrapper(function):
        def inner(doc):
            soup = BeautifulSoup(doc, 'html.parser')
            
def save_pics(html_doc, dir):
    soup = BeautifulSoup(html_doc, 'html.parser')
    for link in soup.find_all('img'):
        src = link.get('src')
        (filename, extension) = os.path.splitext(src)
        if extension[1:] in VALID_EXTENSIONS:
            picture = requests.get(src)
            local_name = os.path.join(dir, get_file_name(filename) + extension)
            with open(local_name, 'wb') as pic:
                pic.write(picture.content)
            soup.replace(src, local_name)
        return soup.prettify()


def download_html(html, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
        return path


if __name__ == '__main__':
    main('https://ru.hexlet.io/courses', 'var\\tmp')