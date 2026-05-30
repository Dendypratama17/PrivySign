import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

APP_ID = "com.privygate.privyid.stg"

last_action = None
last_action_info = None


def find_with_retry(driver, by, locator, max_retry=2, times=2, delay=2, use_last=False):
    global last_action, last_action_info

    attempt = 0
    while attempt <= max_retry:
        if attempt == 0:
            time.sleep(times)

        try:
            element = driver.find_element(by, locator)
            last_action = lambda: driver.find_element(by, locator).click()
            last_action_info = (by, locator)
            return element

        except NoSuchElementException:
            if attempt < max_retry:
                print(f"[Retry {attempt+1}] -> {locator}")
                time.sleep(delay)
                attempt += 1
            else:
                if use_last and last_action:
                    print(f"Execute last action -> by={last_action_info[0]}, locator={last_action_info[1]}")
                    last_action()
                    attempt = 0
                else:
                    raise


def scroll_down(driver, duration=800):
    size = driver.get_window_size()
    start_x = size['width'] // 2
    start_y = int(size['height'] * 0.8)
    end_y = int(size['height'] * 0.2)
    driver.swipe(start_x, start_y, start_x, end_y, duration)


def take_screenshot(driver, test_name):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"screenshots/{test_name}_{timestamp}.png"
    driver.save_screenshot(filename)


def test_Checkout_Personal_Plan_and_Meterai(driver):

    # Personal Plan
    find_with_retry(driver, AppiumBy.XPATH, f'//android.widget.ImageView[@resource-id="{APP_ID}:id/iv_arrow_subs"]', use_last=True).click()

    # Buy Personal Plan
    find_with_retry(driver, AppiumBy.ID, f'{APP_ID}:id/btn_buy_plan', use_last=True).click()

    # Buy Now
    find_with_retry(driver, AppiumBy.ID, f'{APP_ID}:id/btn_buy', use_last=True).click()

    # Add e-Meterai
    find_with_retry(driver, AppiumBy.ID, f'{APP_ID}:id/btn_action', use_last=True).click()

    # Add Amount e-Meterai
    find_with_retry(driver, AppiumBy.ID, f'{APP_ID}:id/iv_add', use_last=True).click()

    # Continue button
    find_with_retry(driver, AppiumBy.XPATH, f'//android.widget.Button[@resource-id="{APP_ID}:id/btn_apply"]', use_last=True).click()

    # Cart
    find_with_retry(driver, AppiumBy.ID, f'{APP_ID}:id/btn_continue', use_last=True).click()

    try:
        find_with_retry(driver, AppiumBy.ID, f'{APP_ID}:id/tv_select_method', max_retry=2)
        scroll_down(driver)
    except NoSuchElementException:
        print("Skip scroll, element not found")

    # Select method
    find_with_retry(driver, AppiumBy.XPATH, f'(//android.widget.ImageView[@resource-id="{APP_ID}:id/iv_check"])[4]', use_last=True).click()

    # Pay
    find_with_retry(driver, AppiumBy.XPATH, f'//android.widget.Button[@resource-id="{APP_ID}:id/btn_pay"]', use_last=True).click()

    # Confirm Payment
    find_with_retry(driver, AppiumBy.ID, f'{APP_ID}:id/btn_action', use_last=True).click()

    title_text = WebDriverWait(driver, 5).until(
        lambda d: d.find_element(AppiumBy.ID, f'{APP_ID}:id/tv_title').text
    )
    expected = ["Checking payments", "Memeriksa pembayaran"]
    assert title_text in expected, f"Expected salah satu dari {expected}, tapi dapat '{title_text}'"


#--------------- Payment Doku ---------------

# def test_Payment_Doku():

#     # Copy VA
#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.privygate.privyid.stg:id/tv_copy_va"]').click()

#     va_number = driver.get_clipboard_text()
#     # print("Copy VA Number:", va_number + "✨")

#     driver.press_keycode(3)

#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.TextView[@content-desc="Chrome"]').click()

#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.android.chrome:id/search_box_text"]').click()

#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.android.chrome:id/url_bar"]').send_keys('https://sandbox.doku.com/integration/simulator/permata-snap/inquiry')

#     find_with_retry(driver, AppiumBy.XPATH, '(//android.widget.TextView[@resource-id="com.android.chrome:id/line_1"])[1]').click()

#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.EditText[@resource-id="virtualAccountNo"]').click()

#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.EditText[@resource-id="virtualAccountNo"]').send_keys(va_number)

#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.Button[@resource-id="btn-submit"]').click()

#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.Button[@resource-id="btnPay"]').click()

#     driver.press_keycode(3)

#     # Dashboard → Privy
#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.TextView[@content-desc="Privy Stg"]').click()

# def test_Confirm_Payment():
#     # Confirm Payment
#     wait = WebDriverWait(driver, 30)
#     find_with_retry(driver, AppiumBy.ID, 'com.privygate.privyid.stg:id/btn_action').click()

#     # take_screenshot(driver, "test_Confirm_Payment")

#     transaction_title = wait.until(
#         EC.presence_of_element_located((AppiumBy.ID, "com.privygate.privyid.stg:id/tv_title"))
#     )
#     expected_texts = ["Transaction completed", "Transaksi selesai"]

#     # Validation text
#     assert transaction_title.text in expected_texts, \
#     f"Teks tidak sesuai. Expected salah satu dari {expected_texts}, tapi dapat '{transaction_title.text}'"

#     print(f"The text that appears: {transaction_title.text} ✨")

#     btns = driver.find_elements(AppiumBy.ID, "com.privygate.privyid.stg:id/btn_activate_now")
#     if btns:
#         btns[0].click()
#         print("Show Activate Now ✨")
#     # else:
#     #     print("the activate now button does not appear ℹ️")

#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.ImageView[@resource-id="com.privygate.privyid.stg:id/btn_toolbar_back"]').click()

#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.ImageView[@resource-id="com.privygate.privyid.stg:id/btn_toolbar_back"]').click()


# # --------------- Buy E-METERAI ---------------

# # E-Meterai
# find_with_retry(driver, AppiumBy.XPATH, '//android.widget.ImageView[@resource-id="com.privygate.privyid.stg:id/iv_arrow_emeterai"]').click()

# # Buy E-Meterai
# find_with_retry(driver, AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.privygate.privyid.stg:id/btn_topup"]').click()

# # Add Amount e-Meterai
# find_with_retry(driver, AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.privygate.privyid.stg:id/tv_3"]').click()

# # Continue button
# find_with_retry(driver, AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.privygate.privyid.stg:id/btn_continue"]').click()

# # Cart - Continue button
# find_with_retry(driver, AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.privygate.privyid.stg:id/btn_continue"]').click()

# # Chevron
# find_with_retry(driver, AppiumBy.XPATH, '(//android.widget.ImageView[@resource-id="com.privygate.privyid.stg:id/iv_chevron"])[4]').click()

# # Select Permata
# find_with_retry(driver, AppiumBy.XPATH, '(//android.widget.ImageView[@resource-id="com.privygate.privyid.stg:id/iv_check"])[6]').click()

# # Pay
# find_with_retry(driver, AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.privygate.privyid.stg:id/btn_pay"]').click()

# # Copy VA
# find_with_retry(driver, AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.privygate.privyid.stg:id/tv_copy_va"]').click()

# va_number = driver.get_clipboard_text()
# print("Copy VA Number:", va_number + "✨")

# driver.press_keycode(3)

# # --------------- Payment Doku ---------------

# find_with_retry(driver, AppiumBy.XPATH, '//android.widget.TextView[@content-desc="Chrome"]').click()

# scroll_down(driver)

# find_with_retry(driver, AppiumBy.XPATH, '//android.widget.Button[@text="BACK TO START"]').click()

# find_with_retry(driver, AppiumBy.XPATH, '//android.widget.EditText[@resource-id="virtualAccountNo"]').click()

# find_with_retry(driver, AppiumBy.XPATH, '//android.widget.EditText[@resource-id="virtualAccountNo"]').send_keys(va_number)

# find_with_retry(driver, AppiumBy.XPATH, '//android.widget.Button[@resource-id="btn-submit"]').click()

# find_with_retry(driver, AppiumBy.XPATH, '//android.widget.Button[@resource-id="btnPay"]').click()

# driver.press_keycode(3)

# # Dashboard → Privy
# find_with_retry(driver, AppiumBy.XPATH, '//android.widget.TextView[@content-desc="Privy Stg"]').click()

# # Confirm Payment
# find_with_retry(driver, AppiumBy.ID, 'com.privygate.privyid.stg:id/btn_action').click()

# # Back to home page
# find_with_retry(driver, AppiumBy.ID, '//android.widget.Button[@resource-id="com.privygate.privyid.stg:id/btn_go_to_home"]').click()


# def test_My_Transaction():

#     # Personal Plan
#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.ImageView[@resource-id="com.privygate.privyid.stg:id/iv_arrow_subs"]').click()

#     # My Transaction
#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.privygate.privyid.stg:id/btn_mytransaction"]').click()

#     # Filter Status Transaction → All status
#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.LinearLayout[@resource-id="com.privygate.privyid.stg:id/v_filter_status"]/android.widget.ImageView').click()

#     take_screenshot(driver, "test_Confirm_Payment")

#     # Select Paid 
#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.privygate.privyid.stg:id/tv_title" and @text="Paid"]').click()

#     # Select Product
#     find_with_retry(driver, AppiumBy.XPATH, '(//android.view.ViewGroup[@resource-id="com.privygate.privyid.stg:id/cl_container"])[1]').click()

#     scroll_down(driver)


# def test_Download_Invoice():

#     # Download Invoice
#     wait = WebDriverWait(driver, 30)
#     find_with_retry(driver, AppiumBy.ID, 'com.privygate.privyid.stg:id/btn_download_invoice').click()

#     take_screenshot(driver, "test_Confirm_Payment")

#     transaction_title = wait.until(
#         EC.presence_of_element_located((AppiumBy.ID, "com.privygate.privyid.stg:id/toast_message"))
#     )

#     # Validation text
#     expected_keywords = ["Saved to Download", "Disimpan di Download"]

#     assert any(keyword in transaction_title.text for keyword in expected_keywords), \
#     f"Text does not match. Expected to contain one of {expected_keywords}, but you can '{transaction_title.text}'"

#     print(f"The text that appears: {transaction_title.text} ✨")


# def test_Download_Receipt():

#     # Download Receipt
#     wait = WebDriverWait(driver, 30)
#     find_with_retry(driver, AppiumBy.ID, 'com.privygate.privyid.stg:id/btn_download_receipt').click()

#     take_screenshot(driver, "test_Confirm_Payment")

#     transaction_title = wait.until(
#         EC.presence_of_element_located((AppiumBy.ID, "com.privygate.privyid.stg:id/toast_message"))
#     )

#     # Validation text
#     expected_keywords = ["Saved to Download", "Disimpan di Download"]

#     assert any(keyword in transaction_title.text for keyword in expected_keywords), \
#     f"Text does not match. Expected to contain one of {expected_keywords}, but you can '{transaction_title.text}'"

#     print(f"The text that appears: {transaction_title.text} ✨")


# def test_Back_To_Dashboard():
#     # Back button to My transaction
#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.ImageView[@resource-id="com.privygate.privyid.stg:id/btn_toolbar_back"]').click()

#     # Back button to Personal plan
#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.ImageView[@resource-id="com.privygate.privyid.stg:id/btn_toolbar_back"]').click()

#     # Back button to Dashboard
#     find_with_retry(driver, AppiumBy.XPATH, '//android.widget.ImageView[@resource-id="com.privygate.privyid.stg:id/btn_toolbar_back"]').click()

#     take_screenshot(driver, "test_Confirm_Payment")
