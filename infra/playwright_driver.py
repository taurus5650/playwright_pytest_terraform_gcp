from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext, TimeoutError
from utils.logger import logger
import os
import time
from typing import List, Union, Optional, Iterable, overload


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

    def page_pause(self):
        logger.info(f'page_pause')
        try:
            return self.page.pause()
        except Exception as e:
            self._handle_exception_screenshot(action='page_pause', exception=e)

    def goto(self, url: str):
        logger.info(f'goto={url}')
        try:
            self.page.goto(url=url)
            return self.page
        except Exception as e:
            self._handle_exception_screenshot(action='goto', exception=e)

    def click(self, selector: str, timeout: int = None):
        logger.info(f'click={selector}')
        try:
            if timeout is None:
                timeout = self.TIMEOUT

            locator = self.page.locator(selector=selector)
            locator.wait_for(state='visible', timeout=timeout)
            return locator.click(timeout=timeout)
        except Exception as e:
            self._handle_exception_screenshot(action='click', exception=e)

    def checkbox_or_radio(self, selector: str, timeout: int = None):
        logger.info(f'checkbox_or_radio={selector}')
        try:
            if timeout is None:
                timeout = self.TIMEOUT

            locator = self.page.locator(selector=selector)
            locator.wait_for(state='attached', timeout=timeout)  # DOM
            locator.wait_for(state='visible', timeout=timeout)  # Waiting CSS done
            return locator.check(timeout=timeout)
        except Exception as e:
            self._handle_exception_screenshot(action='checkbox_or_radio', exception=e)

    def select_option_with_value(self, selector: str, value: Union[str, List[str]], timeout: int = None):  # dropdown list
        logger.info(f'select_option_with_value={selector}')
        try:
            if timeout is None:
                timeout = self.TIMEOUT

            locator = self.page.locator(selector=selector)
            locator.wait_for(state='attached', timeout=timeout)  # DOM
            locator.wait_for(state='visible', timeout=timeout)  # Waiting CSS done
            return locator.select_option(timeout=timeout, value=value)
        except Exception as e:
            self._handle_exception_screenshot(action='click', exception=e)

    def fill(self, selector: str, value: str):
        logger.info(f'fill={selector}')
        try:
            self.page.fill(selector=selector, value=value)
        except Exception as e:
            self._handle_exception_screenshot(action='fill', exception=e)

    def inner_text(self, selector: str, timeout: int = None) -> str:
        logger.info(f'inner_text={selector}')
        try:
            if timeout is None:
                timeout = self.TIMEOUT
            locator = self.page.locator(selector=selector)
            locator.wait_for(state='visible', timeout=timeout)  # Visible = Waiting CSS done (display != None, opcity != 0)
            return locator.inner_text()  # Page's text, including child node
        except Exception as e:
            self._handle_exception_screenshot(action='inner_text', exception=e)

    def close_driver(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()
