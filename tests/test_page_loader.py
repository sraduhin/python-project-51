import pathlib
import tempfile
import os
import re
import pytest

from bs4 import BeautifulSoup

from urllib.parse import urlparse
from page_loader import download
from page_loader.assets import get_content_and_assets, download_assets
from page_loader.urls import create_local_name, get_url, get_url_content
from page_loader.urls import normalize


FIXTURES_DIR = os.path.join('tests', 'fixtures', 'expected')
SOURCE_HTML = os.path.join(FIXTURES_DIR, 'source.html')
RESULT_HTML = os.path.join(FIXTURES_DIR, 'result.html')
URL = 'https://ru.hexlet.io/courses'
URL_HARD = 'https://ru.hexlet.io/n_a.me/to-l_.oc/al-'


@pytest.fixture
def get_html_doc():
    with open(SOURCE_HTML, 'r', encoding='utf-8') as f:
        doc = f.read()
    return doc


@pytest.fixture
def get_html_result():
    with open(RESULT_HTML, 'r', encoding='utf-8') as f:
        doc = f.read()
        doc = BeautifulSoup(doc, 'html.parser')
    return doc.prettify()


@pytest.fixture
def get_html_soup(get_html_doc):
    soup = BeautifulSoup(get_html_doc, 'html.parser')
    return soup


def fake_downloader(*_):
    pass


# test downloader.py
def test_download(requests_mock, get_html_doc, get_html_result):
    downloader = fake_downloader
    expected = get_html_result
    with tempfile.TemporaryDirectory() as tempdir:
        requests_mock.get(URL, text=get_html_doc)
        temp_file = download(URL, tempdir, downloader)
        with open(temp_file, 'r', encoding="utf-8") as tested:
            tested = tested.read()
            assert expected == tested


# test resources
def test_get_content(requests_mock, get_html_doc, get_html_result):
    expected = get_html_result
    requests_mock.get(URL, text=get_html_doc)
    tested, _ = get_content_and_assets(URL)
    assert expected == tested


def test_get_assets(requests_mock):
    script = '/assets/menu.css'
    url = 'https://simple/url.html'
    requests_mock.get(url, text=f'<!DOCTYPE html><link href="{script}"/>')
    _, assets = get_content_and_assets(url)
    print('asdfasdlfkjasdlfkjjas;dlfkjja')
    print(assets)
    assert assets == [
        (f'https://simple{script}', 'simple-url_files/simple-assets-menu.css')
    ]


def test_download_img(requests_mock):
    fixture_path_file = pathlib.Path(FIXTURES_DIR, 'harold_one.png')
    with open(fixture_path_file, 'rb') as expected:
        expected = expected.read()
        requests_mock.get(URL, content=expected)
        with tempfile.TemporaryDirectory() as tempdir:
            temp_file = os.path.join(tempdir, 'temp')
            download_assets([(URL, temp_file)])
            with open(temp_file, 'rb') as tested:
                tested = tested.read()
                assert expected == tested


# test urls.py
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
    assert expected == tested


def test_get_url():
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
        assert get_url(link, URL) == expected[num]


def test_get_url_content(requests_mock, get_html_doc):
    expected = get_html_doc
    requests_mock.get(URL, text=expected)
    tested = get_url_content(URL)
    assert expected == tested.decode('utf-8')


def test_get_invalid_url():
    with pytest.raises(Exception):
        get_url_content(URL_HARD)


'''def test_download_img(requests_mock):
    fixture_path_file = pathlib.Path(FIXTURES_DIR, 'harold_one.png')
    with open(fixture_path_file, 'rb') as expected:
        expected = expected.read()
        with tempfile.TemporaryDirectory() as tempdir:
            temp_file = os.path.join(tempdir, 'temp')
            download_assets(expected, temp_file)
            with open(temp_file, 'rb') as tested:
                tested = tested.read()
                assert expected == tested'''


def test_normalize():
    tested = urlparse(URL_HARD).path
    expected = 'n-a-me-to-l-oc-al'
    assert normalize(tested) == expected
