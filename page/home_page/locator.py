from infra.config import env_config


class Locator(object):

    WEB_BASE_URL = env_config.get('HOMEPAGE', 'WEB_BASE_URL')
    SIGN_IN_OR_SIGN_UP_HYPERLINK = 'xpath=//*[@id="header"]/div/div/div/div[2]/div/ul/li[4]/a'
