from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import datetime
from datetime import timedelta
from selenium.common.exceptions import TimeoutException


email = input("Enter your email: ")
driver = webdriver.Chrome()
driver.get("https://www.tellblazepizza.com/")


current_url = driver.current_url
wait = WebDriverWait(driver, 3)

def wait_for_new_url(driver):
    previous_url = driver.current_url

    def url_changed(driver):
        return driver.current_url != previous_url

    wait = WebDriverWait(driver, 5)
    wait.until(url_changed)

while not driver.current_url.startswith("https://www.tellblazepizza.com/Survey.aspx"):

    next_button = driver.find_element(by="id", value="NextButton")
    next_button.click()

    wait.until(EC.url_changes(current_url))

search_text = "Please provide your email address below to receive your offer. This information will not be used for any other purpose."
page_source = driver.page_source

while search_text not in page_source:
    wait.until(EC.visibility_of_element_located((By.ID, "NextButton")))
    next_button = driver.find_element(by="id", value="NextButton")
    next_button.click()
    wait.until(EC.url_changes(current_url))
    page_source = driver.page_source

send_email = driver.find_element(by="id", value="S000031")
send_email.send_keys(email)

conf_email = driver.find_element(by="id", value="S000032")
conf_email.send_keys(email)

wait.until(EC.visibility_of_element_located((By.ID, "NextButton")))
next_button = driver.find_element(by="id", value="NextButton")
next_button.click()

print(driver.current_url)
input("Press Enter to close the browser...")
driver.quit()