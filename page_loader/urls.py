import requests
import os
import re
from urllib.parse import urlparse

VALID_IMG_EXTENSIONS = ['.png', '.jpg']


def parse_url(url):
    parts = {}
    obj = urlparse(url)
    parts['host'] = obj.hostname
    parts['scheme'] = obj.scheme
    parts['path'] = obj.path
    parts['name'], parts['extension'] = os.path.splitext(parts['path'])
    return parts


def create_local_name(url):
    url_parts = parse_url(url)
    extension = url_parts['extension'] or '.html'
    host = url_parts['host']
    name = normalize(host + url_parts['name'])
    name += extension
    return name


def get_url(url, parent):
    url_parts = parse_url(url)
    if not url_parts['scheme']:
        parents = parse_url(parent)
        url = f"{parents['scheme']}://{parents['host']}{url}"
    return url


def get_url_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def normalize(str: str):
    parts = re.split(r';|_|-|/|\.', str)
    return '-'.join(parts).strip('-.').replace('--', '-')
