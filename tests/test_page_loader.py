import os
import tempfile
import requests_mock
from page_loader.downloader import download


@requests_mock.Mocker()
def test_download(mock):
    url = 'https://ru.hexlet.io/courses'
    excepted_fp = os.path.join('test', 'fixtures', 'expected', 'ru-hexlet-io-courses.html')
    print(excepted_fp)
    with open(excepted_fp, 'r') as f:
        f = f.read()
        print(f)
        mock.get(url, text=f)
        download(url)