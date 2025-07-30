from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext, TimeoutError
from utils import logger
import os
import time


class PlaywrightDriver:

    TIMEOUT = 10000

    def __init__(self, headless: bool = True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def screenshot(self, path: str = None):
        if path is None:
            timestamp = int(time.time())
            path = f'screenshot/{timestamp}.png'
        os.makedirs('screenshot', exist_ok=True)
        self.page.screenshot(path=path)
        logger.info(f'screenshot={path}')

    def _handle_exception_screenshot(self, action: str, exception: str):
        logger.error(f'{action} failed: {exception}')
        self.screenshot()
        raise exception

    def goto(self, url: str):
        logger.info(f'goto={url}')
        try:
            self.page.goto(url=url)
        except Exception as e:
            self._handle_exception_screenshot(action='goto', exception={e})

    def click(self, selector: str, timeout: int = self.TIMEOUT):
        logger.info(f'click={selector}')
        try:
            self.page.locator(selector=selector).click(timeout=timeout)
        except Exception as e:
            self._handle_exception_screenshot(action='click', exception={e})

    def fill(self, selector: str, value: str):
        logger.info(f'fill={selector}')
        try:
            self.page.fill(selector=selector, value=value)
        except Exception as e:
            self._handle_exception_screenshot(action='fill', exception={e})

    def close_driver(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()
