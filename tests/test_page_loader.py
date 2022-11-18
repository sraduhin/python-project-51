import pathlib
import tempfile
import os
import pytest

from bs4 import BeautifulSoup

from urllib.parse import urlparse
from page_loader.utils import (
    download_file,
    download_html,
    find_images,
    find_assets,
    get_host_and_create_local_name,
    get_url,
    normalize,
)
from page_loader import download

FIXTURES_DIR = os.path.join('tests', 'fixtures', 'expected')
FIXTURES_HTML = os.path.join(FIXTURES_DIR, 'source.html')
URL = 'https://ru.someurl.io/n_a.me/to-l_.oc/al-'
FIND_IMAGES_RESULT = [
    "/assets/professions/nodejs.png",
    "/assets/professions/nodejs.jpg",
]
FIND_ASSETS_RESULT = [
    "/assets/application.css",
    "https://ru.hexlet.io/styles/application.css",
    "/courses",
    "https://js.stripe.com/v3/",
    "https://ru.hexlet.io/packs/js/runtime.js",
]

# test downloader.py
'''def test_main_func(requests_mock):
    fixture_source = pathlib.Path(FIXTURES_DIR, 'source.html')
    fixture_result = pathlib.Path(FIXTURES_DIR, 'result.html')
    f = open(pathlib.Path(FIXTURES_DIR, 'files.html'))
    with open(fixture_source, 'r', encoding="utf-8") as html:
        html = html.read()
        for url in FIND_IMAGES_RESULT:
            requests_mock.get(url, content=expected)
        for url in FIND_ASSETS_RESULT:
            requests_mock.get(url, text=expected)
            
        requests_mock.get(URL, text=html)
        sub_urls = find_images()'''
        
    
# test utils.py
def test_get_url(requests_mock):
    with open(FIXTURES_HTML, 'r', encoding="utf-8") as expected:
        expected = expected.read()
        requests_mock.get(URL, text=expected)
        tested = get_url(URL)
        tested = tested.text
        assert expected == tested


def test_download_html():
    with open(FIXTURES_HTML, 'r', encoding="utf-8") as expected:
        expected = expected.read()
        with tempfile.TemporaryDirectory() as tempdir:
            temp_file = os.path.join(tempdir, 'temp')
            download_html(expected, temp_file)
            with open(temp_file, 'r', encoding="utf-8") as tested:
                tested = tested.read()
                assert expected == tested


def test_download_file(requests_mock):
    with open(FIXTURES_HTML, 'r', encoding='utf-8') as expected:
        expected = expected.read()
        requests_mock.get(URL, text=expected)
        with tempfile.TemporaryDirectory() as tempdir:
            temp_file = os.path.join(tempdir, 'temp')
            download_file(URL, temp_file)
            with open(temp_file, 'r', encoding='utf-8') as tested:
                tested = tested.read()
                assert expected == tested


def test_download_img(requests_mock):
    fixture_path_file = pathlib.Path(FIXTURES_DIR, 'harold_one.png')
    with open(fixture_path_file, 'rb') as expected:
        expected = expected.read()
        requests_mock.get(URL, content=expected)
        with tempfile.TemporaryDirectory() as tempdir:
            temp_file = os.path.join(tempdir, 'temp')
            download_file(URL, temp_file, image=True)
            with open(temp_file, 'rb') as tested:
                tested = tested.read()
                assert expected == tested


def test_get_invalid_url():
    with pytest.raises(Exception):
        get_url(URL)


def test_normalize():
    string_part = urlparse(URL).path
    assert normalize(string_part) == 'n-a-me-to-l-oc-al'


def test_get_host_and_create_local_name():
    obj = urlparse(URL)
    hostname = obj.hostname
    path = obj.path
    dirs = ['dir', 'dirin/dir', '']
    exts = ['png', 'jpg', '']
    for dir in dirs:
        for extension in exts:
            print(dir, extension)
            url = '.'.join(['/'.join(['https:/', hostname, path]), extension]).strip('.')
            if dir:
                tested = get_host_and_create_local_name(url, dir)
            else:
                tested = get_host_and_create_local_name(url)
            expected = (
                hostname,
                os.path.join(
                    dir or os.getcwd(),
                    normalize('/'.join([hostname, path]))
                ) + '.' + (extension or 'html'))
            assert tested == expected


def test_find_images():
    with open(FIXTURES_HTML, 'r', encoding='utf-8') as f:
        f = f.read()
        soup = BeautifulSoup(f, 'html.parser')
        assert find_images(soup) == FIND_IMAGES_RESULT


def test_find_assets():
    host = 'ru.hexlet.io'
    with open(FIXTURES_HTML, 'r', encoding='utf-8') as f:
        f = f.read()
        soup = BeautifulSoup(f, 'html.parser')
        expected = find_assets(soup, host)
        assert sorted(expected) == sorted(FIND_ASSETS_RESULT)
