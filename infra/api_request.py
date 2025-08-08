import json
import textwrap
import uuid
import os

import allure
import requests
from pytest import assume

from utility.time import Time
from utils.logger import logger


class BaseAPI:
    GENERAL_WAITING_TIME = 10

    def __init__(self, waiting_time=None):
        self.waiting_time = waiting_time or self.GENERAL_WAITING_TIME
        self._session = requests.Session()

    @allure.step('[{method}] {url}')
    def _send_request(self, method: str, url: str, **kwargs):
        acceptable_waiting_time = kwargs.pop(
            'waiting_time', None) or self.waiting_time

        headers = kwargs.pop('headers', None)
        correlation_id = str(uuid.uuid4()).upper()
        with allure.step(f'Correlation-Id : {correlation_id}'):
            if headers:
                headers['Correlation-Id'] = correlation_id
            else:
                headers = {
                    'Correlation-Id': correlation_id
                }
            try:
                response = self._session.request(
                    method=method, url=url, headers=headers, **kwargs)
                duration = response.elapsed.total_seconds()
                if self.debug_print:
                    self._debug_print(response=response)
            except requests.exceptions.RequestException as e:
                response = None
                logger.error(f'Request Error > url: [{method}] {url}, kwargs: {kwargs}, error: {str(e)}')
            return response

    def _debug_print(self, response: requests.Response):
        req_body = response.request.body
        if req_body:
            try:
                req_body = json.loads(req_body)
            except json.JSONDecodeError:
                pass

        try:
            res = json.dumps(response.json(), indent=4, ensure_ascii=False)
        except json.JSONDecodeError:
            res = response.text

        information = {
            'datetime': f"{Time.now():%Y/%m/%d %H:%M:%S}",
            'request': f"[{response.request.method}] {response.request.url}",
            'headers': json.dumps(
                dict(response.request.headers),
                indent=4,
                ensure_ascii=False
            ),
            'body': json.dumps(
                req_body,
                indent=4,
                ensure_ascii=False
            ),
            'elapsed': f"{response.elapsed.total_seconds()} s",
            'status': response.status_code,
            'response': res}

        logger.info(textwrap.dedent("""
            --------------------------------
            Debug Print
            --------------------------------
            {content}
            --------------------------------
            """).format(content=''.join(
            [f"\n * {key}: {val}" for key, val in information.items()])))
