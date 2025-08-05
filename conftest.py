import logging
import os

import pytest

from utils.logger import logger


def pytest_addoption(parser):
    parser.addoption(
        '--env', action='store', default='test', help='Pytest running environment.'
    )

@pytest.fixture(scope='session', autouse=True)
def set_env(request):
    env_value = request.config.getoption('--env')
    os.environ['ENV'] = env_value  # config.py will detected
    logger.info(f'env={env_value}')