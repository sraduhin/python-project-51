import pathlib
import tempfile
import os
import re
import pytest

from bs4 import BeautifulSoup

from urllib.parse import urlparse
from page_loader.utils import (
    create_local_name,
    download_file,
    download_html,
    find_images,
    find_assets,
    get_html,
    normalize,
    normalize_link,
)

from page_loader import download

FIXTURES_DIR = os.path.join('tests', 'fixtures', 'expected')
SOURCE_HTML = os.path.join(FIXTURES_DIR, 'source.html')
URL = 'https://ru.hexlet.io/n_a.me/to-l_.oc/al-'

@pytest.fixture
def get_html_doc():
    with open(SOURCE_HTML, 'r', encoding='utf-8') as f:
        doc = f.read()
    return doc


@pytest.fixture
def get_html_soup(get_html_doc):
    soup = BeautifulSoup(get_html_doc, 'html.parser')
    return soup

# test downloader.py
def test_download():
    pass

# test utils.py
def test_create_local_name():
    urls = [
        'http://host/path_page',
        'https://host/path_page.ext',
    ]
    expected = [
        os.path.join('host-path-page.html'),
        os.path.join('host-path-page.ext'),
    ]
    tested = []
    for url in urls:
        tested.append(create_local_name(url))
    print(tested)
    assert expected == tested


def test_normalize_link():
    links = [
        '/relative/link.li',
        'https://absolut/link.li',
    ]
    pattern = '(?<=[a-zA-Z0-9])/.*$'
    expected = [
        f"{re.sub(pattern, '', URL)}{links[0]}",
        f'{links[1]}',
    ]
    for num, link in enumerate(links):
        assert normalize_link(link, URL) == expected[num]


def test_get_url(requests_mock, get_html_doc):
    expected = get_html_doc
    requests_mock.get(URL, text=expected)
    tested = get_html(URL)
    tested = tested.text
    assert expected == tested


def test_get_invalid_url():
    with pytest.raises(Exception):
        get_html(URL)


def test_download_html(get_html_doc):
    expected = get_html_doc
    with tempfile.TemporaryDirectory() as tempdir:
        temp_file = os.path.join(tempdir, 'temp')
        download_html(expected, temp_file)
        with open(temp_file, 'r', encoding="utf-8") as tested:
            tested = tested.read()
            assert expected == tested


def test_download_file(requests_mock, get_html_doc):
    expected = get_html_doc
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
            download_file(URL, temp_file)
            with open(temp_file, 'rb') as tested:
                tested = tested.read()
                assert expected == tested


def test_normalize():
    tested = urlparse(URL).path
    expected = 'n-a-me-to-l-oc-al'
    assert normalize(tested) == expected


def test_find_images(get_html_soup):
    expected = [
        "/assets/professions/nodejs.png",
        "/assets/professions/nodejs.jpg",
    ]
    assert sorted(find_images(get_html_soup)) == sorted(expected)


def test_find_assets(get_html_soup):
    expected = [
        "https://ru.hexlet.io/packs/js/runtime.js",
        "/assets/application.css",
        "https://ru.hexlet.io/styles/application.css",
        "/courses",
    ]
    assert sorted(find_assets(get_html_soup, URL)) == sorted(expected)
