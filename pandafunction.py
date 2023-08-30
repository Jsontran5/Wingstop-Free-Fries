from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import time
import datetime
from datetime import timedelta

def panda_survey(email):

    def wait_for_new_url(driver, previous_url, timeout=5):
        def url_changed(driver):
            return driver.current_url != previous_url

        wait = WebDriverWait(driver, timeout)
        wait.until(url_changed)

    driver = webdriver.Chrome()
    driver.get("https://www.pandaguestexperience.com/Index.aspx?POSType=PieceMeal")

    current_url = driver.current_url

    while not driver.current_url.startswith("https://www.pandaguestexperience.com/Survey.aspx"):
        next_button = driver.find_element(by="id", value="NextButton")
        next_button.click()
        wait_for_new_url(driver, current_url)

    search_text = "Please provide your email address to receive your coupon code. This information will not be used for any other purpose. If you do not wish to receive a coupon code, you do not need to provide your email address and can click Next to complete your feedback."
    page_source = driver.page_source

    while search_text not in page_source:
        wait = WebDriverWait(driver, 3)
        wait.until(EC.visibility_of_element_located((By.ID, "NextButton")))
        next_button = driver.find_element(by="id", value="NextButton")
        next_button.click()
        wait_for_new_url(driver, current_url)
        page_source = driver.page_source

    send_email = driver.find_element(by="id", value="S000057")
    send_email.send_keys(email)

    conf_email = driver.find_element(by="id", value="S000064")
    conf_email.send_keys(email)

    wait.until(EC.visibility_of_element_located((By.ID, "NextButton")))
    next_button = driver.find_element(by="id", value="NextButton")
    next_button.click()
   
    if driver.current_url.startswith("https://www.pandaguestexperience.com/Finish.aspx"):
        print("Success! - Panda Express")
        driver.quit()
        return

    input("Press Enter to close the browser...")
    driver.quit()

def main():
    email = input("Enter Email: ")
    panda_survey(email)

if __name__ == "__main__":
    main()
