import os
from configparser import ConfigParser


class EnvConfig:
    def __init__(self):
        env = os.getenv('ENV', 'test').lower()
        cfg_file = os.path.join(os.path.dirname(__file__), '..', 'config', f'{env}.ini')

        parser = ConfigParser()
        parser.read(cfg_file)
        self.parser = parser

    def get(self, section: str, key: str) -> str:
        """Example: get('HOMEPAGE', 'WEB_BASE_URL')"""
        if not self.parser.has_section(section):
            raise KeyError(f'[EnvConfig] Section "{section}" not found.')
        if not self.parser.has_option(section, key):
            raise KeyError(f'[EnvConfig] Key "{key}" not found in section "{section}".')
        return self.parser.get(section, key)

    def get_section(self, section: str) -> dict:
        """Example: get_section('DB_CONFIG') → {'USER': 'myuser', 'PASSWORD': 'secret', 'DATABASE': 'abc_test'}"""
        if not self.parser.has_section(section):
            raise KeyError(f'[EnvConfig] Section "{section}" not found.')
        return dict(self.parser[section])


env_config = EnvConfig()
