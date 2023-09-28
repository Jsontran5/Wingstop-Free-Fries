from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def blaze_pizza_survey(email):
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

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.tellblazepizza.com/")

    current_url = driver.current_url
    wait = WebDriverWait(driver, 3)

    def wait_for_new_url(driver):
        previous_url = driver.current_url

        def url_changed(driver):
            return driver.current_url != previous_url

        wait = WebDriverWait(driver, 3)
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

    if driver.current_url.startswith("https://www.tellblazepizza.com/Finish.aspx"):
        result = "Success! Coupon sent to your email. - Blaze Pizza (works online)"
        driver.quit()
        return result

    print(driver.current_url)
    input("Press Enter to close the browser...")
    driver.quit()

def main():
    email = input("Enter your email: ")
    blaze_pizza_survey(email)

if __name__ == "__main__":
    main()
