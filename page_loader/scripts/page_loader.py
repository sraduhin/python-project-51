#!/usr/bin/env python3
import argparse
import os

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
    print(download(args.url, args.output))


if __name__ == '__main__':
    main()
