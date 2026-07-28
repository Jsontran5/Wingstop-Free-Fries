from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import traceback


def wingstop_survey(email, headless=None):
 
  
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--incognito")
    chrome_options.binary_location = '/opt/render/project/.render/chrome/opt/google/chrome' #UNCOMMENT BEFORE DEPLOYING TO RENDER.COM/PUSHING TO GITHUB
    dotenv_path = '/etc/secrets/.env' #for render.com
    load_dotenv(dotenv_path=dotenv_path) #for render.com

    #load_dotenv()
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://mywingstopsurvey.com/usa?AspxAutoDetectCookieSupport=1")

        wait = WebDriverWait(driver, 10)

        def fill_receipt_code():
            receipt_code = os.getenv("WINGSTOP_CODE", "").strip()
            if len(receipt_code) != 15 or not receipt_code.isdigit():
                raise ValueError(
                    "Set WINGSTOP_CODE to the 15-digit receipt code before running the survey."
                )
            code_chunks = [
                receipt_code[index:index + 3]
                for index in range(0, 15, 3)
            ]
            for index, chunk in enumerate(code_chunks, start=1):
                code_input = wait.until(
                    EC.element_to_be_clickable((By.ID, f"InputUSASmartCode{index}"))
                )
                code_input.clear()
                code_input.send_keys(chunk)

        def click_next_and_wait_for_progress():
            current_url = driver.current_url
            current_source = driver.page_source
            next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
            next_button.click()
            wait.until(
                lambda d: d.current_url != current_url
                or d.page_source != current_source
            )

        fill_receipt_code()

        email_locator = (By.ID, "S000132")
        confirm_email_locator = (By.ID, "S000133")

        while not (
            driver.find_elements(*email_locator)
            and driver.find_elements(*confirm_email_locator)
        ):
            click_next_and_wait_for_progress()

        print("Coupon email screen found.")

        send_email = wait.until(EC.element_to_be_clickable(email_locator))
        send_email.click()
        send_email.clear()
        send_email.send_keys(email)
        wait.until(lambda d: send_email.get_attribute("value") == email)

        conf_email = wait.until(EC.element_to_be_clickable(confirm_email_locator))
        conf_email.click()
        conf_email.clear()
        conf_email.send_keys(email)
        wait.until(lambda d: conf_email.get_attribute("value") == email)

        wait.until(EC.visibility_of_element_located((By.ID, "NextButton")))
        current_url = driver.current_url
        next_button = driver.find_element(by="id", value="NextButton")
        next_button.click()
        wait.until(
            lambda d: d.current_url != current_url
            or "Finish.aspx" in d.current_url
        )

        if "Finish.aspx" in driver.current_url:
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
