import os
import time
import warnings

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

warnings.filterwarnings("ignore", category=DeprecationWarning)

APPIUM_SERVER = os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723/wd/hub")
DEVICE_UDID = os.getenv("DEVICE_UDID", "80732706")

os.makedirs("screenshots", exist_ok=True)


@pytest.fixture(scope="module")
def driver():
    options = UiAutomator2Options()
    options.set_capability("platformName", "Android")
    options.set_capability("udid", DEVICE_UDID)
    options.set_capability("noReset", True)
    options.set_capability("automationName", "UiAutomator2")

    d = webdriver.Remote(APPIUM_SERVER, options=options)
    yield d
    d.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"screenshots/FAILED_{item.name}_{timestamp}.png"
            driver.save_screenshot(filename)
            print(f"\nScreenshot saved: {filename}")
