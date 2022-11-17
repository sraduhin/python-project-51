import pathlib
import tempfile
import os
import pytest

from bs4 import BeautifulSoup

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
from urllib.parse import urlparse

FIXTURES_DIR = 'tests/fixtures/expected'
FIXTURES_HTML = os.path.join(FIXTURES_DIR, 'source.html')
URL = 'https://ru.someurl.io/n_a.me/to-l_.oc/al-'


def test_get_url(requests_mock):
    fixture_path_dir = FIXTURES_DIR.split('/')
    fixture_path_file = pathlib.Path(*fixture_path_dir, 'source.html')
    with open(fixture_path_file, 'r', encoding="utf-8") as expected:
        expected = expected.read()
        requests_mock.get(URL, text=expected)
        tested = get_url(URL)
        tested = tested.text
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
    result = [
        "/assets/professions/nodejs.png",
        "/assets/professions/nodejs.jpg",
    ]
    with open(FIXTURES_HTML, 'r', encoding='utf-8') as f:
        f = f.read()
        soup = BeautifulSoup(f, 'html.parser')
        assert find_images(soup) == result


def test_find_assets():
    host = 'ru.hexlet.io'
    result = [
        "/assets/application.css",
        "https://ru.hexlet.io/styles/application.css",
        "/courses",
        "https://js.stripe.com/v3/",
        "https://ru.hexlet.io/packs/js/runtime.js",
    ]
    with open(FIXTURES_HTML, 'r', encoding='utf-8') as f:
        f = f.read()
        soup = BeautifulSoup(f, 'html.parser')
        expected = find_assets(soup, host)
        assert sorted(expected) == sorted(result)


def test_download_html():
    fixture_path_dir = FIXTURES_DIR.split('/')
    fixture_path_file = pathlib.Path(*fixture_path_dir, 'source.html')
    with open(fixture_path_file, 'r', encoding="utf-8") as expected:
        expected = expected.read()
        print('expected>>>')
        print(expected)
        with tempfile.TemporaryDirectory() as tempdir:
            test_path_file = download_html(expected, tempdir)
            with open(test_path_file, 'r', encoding="utf-8") as tested:
                tested = tested.read()
                print('tested>>>')
                print(tested)
                assert expected == tested
