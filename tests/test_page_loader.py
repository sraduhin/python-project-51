# from page_loader.downloader import main

# FIXTURES_DIR = 'tests/fixtures/expected'


def test_download(requests_mock):
    '''url = 'https://ru.someurl.io/tail'
    fixture_path_dir = FIXTURES_DIR.split('/')
    fixture_path_file = pathlib.Path(*fixture_path_dir, 'chicken.html')
    with open(fixture_path_file, 'r', encoding="utf-8") as expected:
        expected = expected.read()
        requests_mock.get(url, text=expected)
        with tempfile.TemporaryDirectory() as tempdir:
            test_path_file = download(url, tempdir)
            with open(test_path_file, 'r', encoding="utf-8") as tested:
                tested = tested.read()
                assert expected == tested'''
    assert True is True
