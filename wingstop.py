from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import datetime
from datetime import timedelta
from selenium.common.exceptions import TimeoutException

email = input("Enter Email: ")
driver = webdriver.Chrome()
driver.get("https://mywingstopsurvey.com/usa")


current_url = driver.current_url

def wait_for_new_url(driver):
    previous_url = driver.current_url

    def url_changed(driver):
        return driver.current_url != previous_url

    wait = WebDriverWait(driver, 5)
    wait.until(url_changed)

yesterday = datetime.datetime.now() - timedelta(days=1)
yesterday_date = yesterday.strftime("%d")

while not driver.current_url.startswith("https://mywingstopsurvey.com/Survey.aspx"):
    
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
    meridian_dropdown.select_by_value("AM")

    order = driver.find_element(by="id", value="InputTransactionNum")
    order.send_keys("567")
    order.send_keys(Keys.TAB)

    next_button = driver.find_element(by="id", value="NextButton")
    next_button.click()

    wait.until(EC.url_changes(current_url))
  


wait.until(EC.visibility_of_element_located((By.ID, "NextButton")))
next_button = driver.find_element(by="id", value="NextButton")
next_button.click()
wait.until(EC.url_changes(current_url))

satisfied_option = driver.find_element(by="id", value="ANS000473.5")
satisfied_option.click()


in_restaurant_radio = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[text()='In restaurant']")))
in_restaurant_radio.click()

wait = WebDriverWait(driver, 3)
pickup_option_radio = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[text()='Pick up a carry out order in-store']")))
pickup_option_radio.click()


wait_for_new_url(driver)
next_buttons = wait.until(EC.presence_of_all_elements_located((By.ID, "NextButton")))
print(len(next_buttons))
if next_buttons:
    last_next_button = next_buttons[-1]
    last_next_button.click()
wait_for_new_url(driver)
next_buttons = wait.until(EC.presence_of_all_elements_located((By.ID, "NextButton")))
print(len(next_buttons))
if next_buttons:
    last_next_button = next_buttons[-1]
    last_next_button.click()

wait_for_new_url(driver)

try:
    visit = EC.element_to_be_clickable((By.XPATH, "//label[text()='More often']"))
    visit.click()  
except:
    wait = WebDriverWait(driver, 3)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "radioSimpleInput")))
    radio_button = driver.find_elements(By.CLASS_NAME, "radioSimpleInput")
    radio_button[len(radio_button)-1].click()
    wait_for_new_url(driver)
    radio_button = driver.find_elements(By.CLASS_NAME, "radioSimpleInput")
    print(len(radio_button))
    radio_button[len(radio_button)-1].click()

wait_for_new_url(driver)

next_buttons = wait.until(EC.presence_of_all_elements_located((By.ID, "NextButton")))
print(len(next_buttons))
if next_buttons:
    last_next_button = next_buttons[-1]
    last_next_button.click()

wait_for_new_url(driver)
send_email = driver.find_element(by="id", value="S000132")
send_email.send_keys(email)

conf_email = driver.find_element(by="id", value="S000133")
conf_email.send_keys(email)

next_buttons = wait.until(EC.presence_of_all_elements_located((By.ID, "NextButton")))
print(len(next_buttons))
if next_buttons:
    last_next_button = next_buttons[-1]
    last_next_button.click()




print(driver.current_url)
input("Press Enter to close the browser...")
driver.quit()