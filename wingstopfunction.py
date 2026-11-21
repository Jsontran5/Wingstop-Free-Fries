from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import gc
import os
import shutil
import subprocess
import tempfile
import traceback


def wingstop_survey(email, headless=None):
    # Configure Chrome to run in headless mode with low-memory flags
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--disk-cache-size=1")
    chrome_options.add_argument("--media-cache-size=1")
    chrome_options.add_argument("--renderer-process-limit=1")
    chrome_options.add_argument("--js-flags=--max-old-space-size=128")

    chrome_options.binary_location = '/opt/render/project/.render/chrome/opt/google/chrome/google-chrome' #UNCOMMENT BEFORE DEPLOYING TO RENDER.COM/PUSHING TO GITHUB
    dotenv_path = '/etc/secrets/.env' #for render.com
    load_dotenv(dotenv_path=dotenv_path) #for render.com

    #load_dotenv()
    driver = None
    user_data_dir = tempfile.mkdtemp(prefix="wingstop_chrome_")
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
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

            # Wingstop now defaults to a 20-digit code page (CN1..CN7) with a link (a.InviteChanger)
            # to switch to the 15-digit code page (CN1..CN5).
            wait.until(
                lambda d: d.find_elements(By.ID, "CN1")
                or d.find_elements(By.ID, "InputUSASmartCode1")
                or d.find_elements(By.CSS_SELECTOR, "a.InviteChanger")
            )
            if driver.find_elements(By.ID, "CN6"):
                switcher = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.InviteChanger"))
                )
                switcher.click()
                wait.until(
                    lambda d: not d.find_elements(By.ID, "CN6")
                    and (
                        d.find_elements(By.ID, "CN1")
                        or d.find_elements(By.ID, "InputUSASmartCode1")
                    )
                )

            code_chunks = [
                receipt_code[index:index + 3]
                for index in range(0, 15, 3)
            ]
            use_cn_inputs = bool(driver.find_elements(By.ID, "CN1"))
            for index, chunk in enumerate(code_chunks, start=1):
                input_id = f"CN{index}" if use_cn_inputs else f"InputUSASmartCode{index}"
                code_input = wait.until(
                    EC.element_to_be_clickable((By.ID, input_id))
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

        loop_count = 0
        while not (
            driver.find_elements(*email_locator)
            and driver.find_elements(*confirm_email_locator)
        ):
            loop_count += 1
            if loop_count > 30:
                raise Exception("Blocked or stuck on Wingstop survey.")
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
            try:
                driver.quit()
            except Exception:
                pass
        if os.name != "nt" and user_data_dir:
            try:
                subprocess.run(["pkill", "-9", "-f", user_data_dir], check=False)
            except Exception:
                pass
        if user_data_dir:
            shutil.rmtree(user_data_dir, ignore_errors=True)
        gc.collect()

    return result

def main():
    email = input("Enter your email: ")
    result = wingstop_survey(email)
    print(result)

if __name__ == "__main__":
    main()
