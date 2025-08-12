import os
from configparser import ConfigParser


class EnvConfig:
    def __init__(self):
        env = os.getenv('ENV', 'test').lower()
        cfg_file = os.path.join(os.path.dirname(__file__), '..', 'config', f'{env}.ini')

        parser = ConfigParser()
        parser.optionxform = str
        parser.read(cfg_file)
        self.parser = parser

    def get_single_key(self, section: str, key: str) -> str:
        """Example: get_single_key('HOMEPAGE', 'WEB_BASE_URL')"""
        if not self.parser.has_section(section):
            raise KeyError(f'[EnvConfig] Section "{section}" not found.')
        if not self.parser.has_option(section, key):
            raise KeyError(f'[EnvConfig] Key "{key}" not found in section "{section}".')
        return self.parser.get(section, key)

    def get_dict_key(self, section: str) -> dict:
        """Example: get_dict_key('DB_CONFIG') → {'USER': 'myuser', 'PASSWORD': 'secret', 'DATABASE': 'abc_test'}"""
        if not self.parser.has_section(section):
            raise KeyError(f'[EnvConfig] Section "{section}" not found.')
        return dict(self.parser[section])


_env_config = None
def get_env_config():
    global _env_config
    if _env_config is None:
        _env_config = EnvConfig()
    return _env_config
