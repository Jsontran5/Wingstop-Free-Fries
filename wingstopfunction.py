from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
from datetime import timedelta
import os
import traceback


def wingstop_survey(email, headless=None):
 
    # Configure Chrome to run in headless mode
    chrome_options = webdriver.ChromeOptions()

    if headless is None:
        headless = os.getenv("WINGSTOP_HEADLESS", "1") != "0"

    if headless:
        headless_mode = os.getenv("WINGSTOP_HEADLESS_MODE", "new")
        chrome_options.add_argument(f"--headless={headless_mode}" if headless_mode else "--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_argument("--incognito")
    chrome_options.binary_location = '/opt/render/project/.render/chrome/opt/google/chrome' #UNCOMMENT BEFORE DEPLOYING TO RENDER.COM/PUSHING TO GITHUB

    driver = None
    def wait_for_new_url(driver, previous_url, timeout=5):
        def url_changed(driver):
            return driver.current_url != previous_url

        wait = WebDriverWait(driver, timeout)
        wait.until(url_changed)

    #driver = webdriver.Chrome()
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://mywingstopsurvey.com/usa")

        wait = WebDriverWait(driver, 10)

        def click_next_and_wait_for_progress():
            current_url = driver.current_url
            current_source = driver.page_source
            next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
            next_button.click()
            wait.until(
                lambda d: d.current_url != current_url
                or d.page_source != current_source
            )

        while not driver.current_url.startswith("https://mywingstopsurvey.com/Survey.aspx"):
            click_next_and_wait_for_progress()

        search_text = "Please fill out your coupon email below.  This information will not be used for any other purpose."
        page_source = driver.page_source

        while search_text not in page_source:
            click_next_and_wait_for_progress()
            page_source = driver.page_source

        send_email = driver.find_element(by="id", value="S000132")
        send_email.send_keys(email)

        conf_email = driver.find_element(by="id", value="S000133")
        conf_email.send_keys(email)

        wait.until(EC.visibility_of_element_located((By.ID, "NextButton")))
        current_url = driver.current_url
        next_button = driver.find_element(by="id", value="NextButton")
        next_button.click()
        wait.until(
            lambda d: d.current_url != current_url
            or d.current_url.startswith("https://mywingstopsurvey.com/Finish.aspx")
        )

        if driver.current_url.startswith("https://mywingstopsurvey.com/Finish.aspx"):
            result = "Success! Coupon sent to your email. - Wingstop (works online)"
        else:
            result = "Unexpected page encountered."

    except Exception as e:
        traceback.print_exc()
        result = f"An error occurred: {str(e)}"
    finally:
        if driver:
            driver.quit()

    return result

def main():
    email = input("Enter your email: ")
    result = wingstop_survey(email)
    print(result)

if __name__ == "__main__":
    main()
