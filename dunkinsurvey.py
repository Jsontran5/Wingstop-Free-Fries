from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time
import datetime

def dunkin_survey(email):
    chrome_options = webdriver.ChromeOptions()

    #chrome_options.add_argument("--headless")
   # chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
   # chrome_options.add_argument("--ignore-certificate-errors")
    #chrome_options.add_argument("--disable-extensions")
    #chrome_options.add_argument("--no-sandbox")
   # chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_argument("--incognito")
    #chrome_options.binary_location = '/opt/render/project/.render/chrome/opt/google/chrome' #for render.com
    driver = webdriver.Chrome(options=chrome_options)
    
    def wait_for_new_url(driver, previous_url, timeout=5):
        def url_changed(driver):
            return driver.current_url != previous_url

        wait = WebDriverWait(driver, timeout)
        wait.until(url_changed)

    try:
        driver.get("https://survey3.medallia.com/?dunkin-dd-live1")

        current_url = driver.current_url
        wait = WebDriverWait(driver, 3)

        yesterday = datetime.datetime.now() - timedelta(days=1)
        yesterday_date = yesterday.strftime("%d")

        while not driver.current_url.startswith("https://survey3.medallia.com/?feedless-dunkin"):
            
            search = driver.find_element(by="id", value="InputStoreNum")
            search.send_keys("363570")
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

        search_text = "Please provide your email address below to receive your offer. This information will not be used for any other purpose."
        page_source = driver.page_source

        while search_text not in page_source:
            wait.until(EC.visibility_of_element_located((By.ID, "NextButton")))
            next_button = driver.find_element(by="id", value="NextButton")
            next_button.click()
            wait_for_new_url(driver, current_url)
            page_source = driver.page_source

        send_email = driver.find_element(by="id", value="S000031")
        send_email.send_keys(email)

        conf_email = driver.find_element(by="id", value="S000032")
        conf_email.send_keys(email)

        wait.until(EC.visibility_of_element_located((By.ID, "NextButton")))
        next_button = driver.find_element(by="id", value="NextButton")
        next_button.click()

        if driver.current_url.startswith("https://www.tellblazepizza.com/Finish.aspx"):
            result = "Success! Coupon sent to your email. - Dunkin' (at store only)"
        else:
            result = "Unexpected page encountered."

    except Exception as e:
        result = f"An error occurred: {str(e)}"
    finally:
        driver.quit()

    return result

def main():
    email = input("Enter your email: ")
    result = dunkin_survey(email)
    print(result)

if __name__ == "__main__":
    main()