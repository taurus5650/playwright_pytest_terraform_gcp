class Locator(object):

    SIGN_IN_OR_SIGN_UP_PAGE_H2 = 'h2:has-text("New User Signup!")'  # CSS + Text selector (Only Playwright)
    SIGN_UP_NAME = '[data-qa="signup-name"]'  # CSS_SELECTOR
    SIGN_UP_EMAIL = '[data-qa="signup-email"]'  # CSS_SELECTOR
    SIGN_UP_BTN = '[data-qa="signup-button"]'  # CSS_SELECTOR
    EMAIL_ADDRESS_ALR_EXIST = '//*[@id="form"]/div/div/div[3]/div/form/p'  # XPath
