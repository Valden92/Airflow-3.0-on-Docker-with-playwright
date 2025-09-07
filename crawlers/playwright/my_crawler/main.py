"""
My playwright crawler.
"""

import logging
from typing import Any

from playwright.sync_api import sync_playwright

from crawlers.base.const import LOGGING


def main() -> None:
    """Main crawler function."""

    logging.info('Start crawler...')
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)

        try:
            for i in start_crawling():
                logging.info(f'Parse page {i}')
        except Exception:
            logging.error('Error, when trying to crawling!')
            raise
        finally:
            browser.close()
    logging.info('End crawler.')


def start_crawling() -> Any:
    """Some crawl logic."""

    for i in range(1, 10):
        yield i


if __name__ == '__main__':
    logging.basicConfig(**LOGGING)
    main()
