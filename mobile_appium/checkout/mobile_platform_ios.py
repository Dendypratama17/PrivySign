from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import time

desired_caps = {
    'platformName': 'iOS',
    'udid': '00008110-001C493A0AFA801E',
    'noReset': True,
    'automationName': 'automationName'
}

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

try:
    driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@content-desc="Privy"]').click()
    time.sleep(3)


finally:
    driver.quit()
