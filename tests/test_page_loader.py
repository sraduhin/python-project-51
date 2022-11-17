import pathlib
import tempfile
import os
import pytest

from page_loader.utils import get_url, get_host_and_create_local_name, normalize
from page_loader import download
from urllib.parse import urlparse

FIXTURES_DIR = 'tests/fixtures/expected'
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



'''
def test_download(requests_mock):
    fixture_path_dir = FIXTURES_DIR.split('/')
    fixture_path_file = pathlib.Path(*fixture_path_dir, 'source.html')
    with open(fixture_path_file, 'r', encoding="utf-8") as expected:
        expected = expected.read()
        requests_mock.get(URL, text=expected)
        with tempfile.TemporaryDirectory() as tempdir:
            test_path_file = download(URL, tempdir)
            with open(test_path_file, 'r', encoding="utf-8") as tested:
                tested = tested.read()
                assert expected == tested'''
