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


def wingstop_survey(email):
 
    # Configure Chrome to run in headless mode
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_argument("--incognito")
    chrome_options.binary_location = '/opt/render/project/.render/chrome/opt/google/chrome' #UNCOMMENT BEFORE DEPLOYING TO RENDER.COM/PUSHING TO GITHUB

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://mywingstopsurvey.com/usa")

        current_url = driver.current_url
        wait = WebDriverWait(driver, 3)

        while not driver.current_url.startswith("https://mywingstopsurvey.com/Survey.aspx"):
            next_button = driver.find_element(by="id", value="NextButton")
            next_button.click()
            wait.until(EC.url_changes(current_url))

        search_text = "Please fill out your coupon email below.  This information will not be used for any other purpose."
        page_source = driver.page_source

        while search_text not in page_source:
            wait.until(EC.visibility_of_element_located((By.ID, "NextButton")))
            next_button = driver.find_element(by="id", value="NextButton")
            next_button.click()
            wait.until(EC.url_changes(current_url))
            page_source = driver.page_source

        send_email = driver.find_element(by="id", value="S000132")
        send_email.send_keys(email)

        conf_email = driver.find_element(by="id", value="S000133")
        conf_email.send_keys(email)

        wait.until(EC.visibility_of_element_located((By.ID, "NextButton")))
        next_button = driver.find_element(by="id", value="NextButton")
        next_button.click()

        if driver.current_url.startswith("https://mywingstopsurvey.com/Finish.aspx"):
            result = "Success! - Wingstop"
        else:
            result = "Unexpected page encountered."

    except Exception as e:
        result = f"An error occurred: {str(e)}"
    finally:
        driver.quit()

    return result

def main():
    email = input("Enter your email: ")
    result = wingstop_survey(email)
    print(result)

if __name__ == "__main__":
    main()
