import os
from configparser import ConfigParser


class EnvConfig:
    def __init__(self):
        env = os.getenv('ENV', 'test').lower()
        cfg_file = os.path.join(os.path.dirname(__file__), '..','config', f'{env}.ini')

        parser = ConfigParser()
        parser.read(cfg_file)
        self.parser = parser

    def get(self, section: str, key: str) -> str:
        """Example: get('HOMEPAGE', 'WEB_BASE_URL')"""
        return self.parser[section][key]


env_config = EnvConfig()
