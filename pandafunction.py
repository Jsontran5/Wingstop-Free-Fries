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
from dotenv import load_dotenv
import os

def panda_survey(email):
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_argument("--incognito")
    chrome_options.binary_location = '/opt/render/project/.render/chrome/opt/google/chrome' #for render.com
    
    dotenv_path = '/etc/secrets/.env' #for render.com
    load_dotenv(dotenv_path=dotenv_path) #for render.com

    #load_dotenv()

    driver = webdriver.Chrome(options=chrome_options)
    
    def wait_for_new_url(driver, previous_url, timeout=5):
        def url_changed(driver):
            return driver.current_url != previous_url

        wait = WebDriverWait(driver, timeout)
        wait.until(url_changed)

    try:
        driver.get("https://www.pandaguestexperience.com/")

        current_url = driver.current_url
       
        blocked = False
        while not driver.current_url.startswith("https://www.pandaguestexperience.com/Survey.aspx"):
            if driver.current_url.startswith("https://www.pandaguestexperience.com/Block.aspx"):
                #print("Blocked, restarting...")
                if driver:
                    driver.quit()
                return "Blocked"
                blcoked = True
                driver.quit()
                driver = webdriver.Chrome(options=chrome_options)
                driver.get("https://www.pandaguestexperience.com/")

                current_url = driver.current_url
                continue
            if blocked:
                code_parts = os.getenv("BLOCKED_CODES").split(",")
            else:
                code_parts = os.getenv("NORMAL_CODES").split(",")
   

            driver.find_element(By.ID, "CN1").send_keys(code_parts[0])
            driver.find_element(By.ID, "CN2").send_keys(code_parts[1])
            driver.find_element(By.ID, "CN3").send_keys(code_parts[2])
            driver.find_element(By.ID, "CN4").send_keys(code_parts[3])
            driver.find_element(By.ID, "CN5").send_keys(code_parts[4])
            driver.find_element(By.ID, "CN6").send_keys(code_parts[5])

       

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
            result = "Success! Coupon sent to your email. - Panda Express (works online)"
        else:
            result = "Unexpected page encountered."

    except Exception as e:
        result = f"An error occurred: {str(e)}"
    finally:
        driver.quit()

    return result

def main():
    email = input("Enter Email: ")
    result = panda_survey(email)
    print(result)

if __name__ == "__main__":
    main()
