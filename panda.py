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

email = input("Enter Email: ")
driver = webdriver.Chrome()
driver.get("https://www.pandaguestexperience.com/Index.aspx?POSType=PieceMeal")


current_url = driver.current_url

def wait_for_new_url(driver):
    previous_url = driver.current_url

    def url_changed(driver):
        return driver.current_url != previous_url

    wait = WebDriverWait(driver, 5)
    wait.until(url_changed)

yesterday = datetime.datetime.now() - timedelta(days=1)
yesterday_date = yesterday.strftime("%d")


    
search = driver.find_element(by="id", value="InputStoreNum")
search.send_keys("623")
search.send_keys(Keys.TAB)

datepicker_trigger = driver.find_element(by="class name", value="ui-datepicker-trigger")
datepicker_trigger.click()

wait = WebDriverWait(driver, 3)
datepicker = wait.until(EC.visibility_of_element_located((By.ID, "ui-datepicker-div")))


desired_date = datepicker.find_element(by="xpath", value=f"//a[@data-date='{yesterday_date}']")
desired_date.click()

hour_select = driver.find_element(by="name", value="InputHour")
hour_dropdown = Select(hour_select)
hour_dropdown.select_by_value("03")

minute_select = driver.find_element(by="id", value="InputMinute")
minute_dropdown = Select(minute_select)
minute_dropdown.select_by_value("23")

meridian_select = driver.find_element(by="id", value="InputMeridian")
meridian_dropdown = Select(meridian_select)
meridian_dropdown.select_by_value("PM")

order = driver.find_element(by="id", value="InputOrderNum")
order.send_keys("567")
order.send_keys(Keys.TAB)

while not driver.current_url.startswith("https://www.pandaguestexperience.com/Survey.aspx"):

    next_button = driver.find_element(by="id", value="NextButton")
    next_button.click()

    wait.until(EC.url_changes(current_url))

search_text = "Please provide your email address to receive your coupon code. This information will not be used for any other purpose. If you do not wish to receive a coupon code, you do not need to provide your email address and can click Next to complete your feedback."
page_source = driver.page_source

while search_text not in page_source:
    wait.until(EC.visibility_of_element_located((By.ID, "NextButton")))
    next_button = driver.find_element(by="id", value="NextButton")
    next_button.click()
    wait.until(EC.url_changes(current_url))
    page_source = driver.page_source


send_email = driver.find_element(by="id", value="S000057")
send_email.send_keys(email)

conf_email = driver.find_element(by="id", value="S000064")
conf_email.send_keys(email)

wait.until(EC.visibility_of_element_located((By.ID, "NextButton")))
next_button = driver.find_element(by="id", value="NextButton")
next_button.click()

print(driver.current_url)
input("Press Enter to close the browser...")
driver.quit()