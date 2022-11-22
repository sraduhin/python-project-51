#!/usr/bin/env python3
import argparse
import os
import logging
import sys
from page_loader import download


def main():
    parser = argparse.ArgumentParser(
        description='HTML-page downloader'
    )
    parser.add_argument('url', help="page's URL")
    parser.add_argument(
        '-o', '--output', help='download path', default=os.getcwd()
    )
    args = parser.parse_args()
    try:
        path = download(args.url, args.output)
    except Exception as err:
        logging.error(f'Error occurred: {err}')
        return sys.exit(1)

    print(path)


if __name__ == '__main__':
    main()
