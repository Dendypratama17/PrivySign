from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_login():

    # driver = webdriver.Chrome()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    try:

        driver.get("https://oauth2.privypass.id/")

        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/form/div[1]/div[2]/div/input"))).send_keys("TES5690")

        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/form/button"))).click()

        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/form/div[2]/div[2]/div/input"))).send_keys("Akuntes1*")

        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/form/button"))).click()

        assert "PrivySign" in driver.title

        print("Test Passed")
        print(driver.title)

    finally:
        driver.quit()