import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import time
import datetime
from datetime import timedelta
import pytz
from dotenv import load_dotenv
import os
from pathlib import Path
import random

def panda_survey(email):
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--incognito")
    
    # Render.com support
    options.binary_location = '/opt/render/project/.render/chrome/opt/google/chrome'
    load_dotenv(dotenv_path='/etc/secrets/.env')

    # load_dotenv()

    # Use undetected-chromedriver
    driver = uc.Chrome(options=options, version_main=152)
    
    def wait(timeout=10):
        return WebDriverWait(driver, timeout)

    def clear_and_type(element, value):
        element.clear()
        element.send_keys(value)

    def try_select(select_element, *values):
        dropdown = Select(select_element)
        last_error = None
        for value in values:
            try:
                dropdown.select_by_visible_text(value)
                return
            except Exception as e:
                last_error = e
            try:
                dropdown.select_by_value(value)
                return
            except Exception as e:
                last_error = e
        raise last_error

    try:
        driver.get("https://www.pandaguestexperience.com/?POSType=PieceMeal")

        # Wait for either the block page or the receipt entry / survey page
        time.sleep(3)

        if "Block.aspx" in driver.current_url:
            return "Blocked before receipt entry."

        # If we need to enter receipt info
        try:
            store_input = wait(5).until(EC.presence_of_element_located((By.ID, "InputStoreNum")))
            
            store_num = os.getenv("PANDA_STORE")
            today = datetime.datetime.now(pytz.timezone("America/Los_Angeles")).date()
            visit_date = today - timedelta(days=1)
            hour = os.getenv("PANDA_TIME_HOUR").zfill(2)
            minute = os.getenv("PANDA_TIME_MINUTE").zfill(2)
            meridian = os.getenv("PANDA_TIME_MERIDIAN")
            order_num = os.getenv("PANDA_ORDER")
            
            display_date = visit_date.strftime("%m/%d/%Y")
            clear_and_type(store_input, store_num)
            
            date_input = driver.find_element(By.ID, "Index_VisitDateDatePicker")
            driver.execute_script("arguments[0].removeAttribute('readonly')", date_input)
            clear_and_type(date_input, display_date)
            
            try_select(driver.find_element(By.ID, "InputHour"), hour)
            try_select(driver.find_element(By.ID, "InputMinute"), minute)
            try_select(driver.find_element(By.ID, "InputMeridian"), meridian)
            clear_and_type(driver.find_element(By.ID, "InputOrderNum"), order_num)
            
            print(f"Submitting: Store {store_num}, Date {display_date}, Time {hour}:{minute} {meridian}, Order {order_num}")
            
            wait(5).until(EC.element_to_be_clickable((By.ID, "NextButton"))).click()
            time.sleep(3)
            
            if "Block.aspx" in driver.current_url:
                print("Blocked after submitting receipt.")
                return "Blocked after receipt entry."
        except TimeoutException:
            # If there's no receipt form, just continue to the next step
            pass

        # Now just loop through the survey clicking 'NextButton' until email field appears
        search_text = "Please provide your email address to receive your coupon code."
        
        while search_text not in driver.page_source:
            if "Block.aspx" in driver.current_url:
                driver.save_screenshot("panda_diagnostics/blocked_survey.png")
                return "Blocked during survey."
            try:
                # Find all radio buttons. We'll just click the first one we see.
                # Actually, SMG uses `<div class="radioSimpleInput">` or similar. Let's just use JS to find one label per radio group and click it safely without checking all checkboxes.
                driver.execute_script('''
                    var groups = {};
                    var radios = document.querySelectorAll("input[type='radio']");
                    for (var i = 0; i < radios.length; i++) {
                        var name = radios[i].name;
                        if (!groups[name]) groups[name] = [];
                        groups[name].push(radios[i]);
                    }
                    for (var name in groups) {
                        // Just click the highest rating (last radio) or first radio
                        var r = groups[name][groups[name].length - 1];
                        var label = r.closest("label") || r.parentElement;
                        if (label) {
                            label.click();
                        } else {
                            r.click();
                        }
                    }
                ''')
                
                next_btn = wait(5).until(EC.element_to_be_clickable((By.ID, "NextButton")))
                
                time.sleep(1) # small pause before next
                driver.save_screenshot(f"panda_diagnostics/page_{time.time()}.png")
                next_btn.click()
                time.sleep(2) # Wait for next page to load
            except Exception as e:
                # Might be at the end or stuck
                break

        if search_text in driver.page_source:
            send_email = driver.find_element(By.ID, "S000057")
            send_email.send_keys(email)

            conf_email = driver.find_element(By.ID, "S000064")
            conf_email.send_keys(email)

            driver.find_element(By.ID, "NextButton").click()
            time.sleep(3)
            
            if "Finish.aspx" in driver.current_url:
                result = "Success! Coupon sent to your email. - Panda Express (works online)"
            else:
                result = "Unexpected page encountered after email submission."
        else:
            result = "Could not find the email submission form."

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
