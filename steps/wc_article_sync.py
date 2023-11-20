
from core.core import *
from core.variable import *
from core.pages import *


logfiles = []
zephyr_report = ""
loggings()

@step('that article is added in woocom')
def step_impl(context):
    context.step_name = "When that article is added in woocom"
    logging.info('Starting Scenario: ' + str(context.scenario))
    logging.info('Starting automation for step: ' + str(context.step_name))
    browser.get(woocom_link)
    browser.find_element(By.ID, 'user_login').send_keys('hdiaz_eshwg1jf')
    browser.find_element(By.ID, 'user_pass').send_keys('foM~?g6~47x6XEGE')
    browser.find_element(By.ID, 'wp-submit').click()
    time.sleep(20)
@step('article should be in woocom ocs')
def step_impl(context):
    pass

@step('article should be in woocom dynamodb')
def step_impl(context):
    pass

@step('OCS-T16XX should be updated to Zephyr')
def step_impl(context):
    pass

