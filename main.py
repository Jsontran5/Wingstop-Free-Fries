from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Chrome()
driver.get("https://mywingstopsurvey.com/usa")

print(driver.title)
current_url = driver.current_url

while not driver.current_url.startswith("https://mywingstopsurvey.com/Survey.aspx"):

    search = driver.find_element(by="id", value="InputStoreNum")

    search.send_keys("623")
    search.send_keys(Keys.TAB)

    datepicker_trigger = driver.find_element(by="class name", value="ui-datepicker-trigger")
    datepicker_trigger.click()

    wait = WebDriverWait(driver, 10)
    datepicker = wait.until(EC.visibility_of_element_located((By.ID, "ui-datepicker-div")))


    desired_date = datepicker.find_element(by="xpath", value="//a[@data-date='18']")
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

wait.until(EC.url_changes(current_url))
order_type = driver.find_element(by="id", value="R000007.2")
order_type.click()

wait.until(EC.visibility_of_element_located((By.ID, "R000008.2")))
eat_location = driver.find_element(by="id", value="R000008.2")
eat_location.click()


wait.until(EC.visibility_of_element_located((By.ID, "FNSR000020")))
food_type = driver.find_element(by="id", value="FNSR000020")
food_type.click()

wait.until(EC.visibility_of_element_located((By.ID, "NextButton")))
next_button = driver.find_element(by="id", value="NextButton")
next_button.click()

wait.until(EC.visibility_of_element_located((By.ID, "FNSR000236")))
flavor_type = driver.find_element(by="id", value="FNSR000236")
flavor_type.click()

wait.until(EC.visibility_of_element_located((By.ID, "NextButton")))
next_button = driver.find_element(by="id", value="NextButton")
next_button.click()

wait.until(EC.visibility_of_element_located((By.ID, "FNSR000505")))
went_well = driver.find_element(by="id", value="FNSR000505")
went_well.click()

wait.until(EC.visibility_of_element_located((By.ID, "NextButton")))
next_button = driver.find_element(by="id", value="NextButton")
next_button.click()

wait.until(EC.visibility_of_element_located((By.ID, "R000521.1")))
more_often = driver.find_element(by="id", value="R000521.1")
more_often.click()

print(driver.current_url)
input("Press Enter to close the browser...")
driver.quit()