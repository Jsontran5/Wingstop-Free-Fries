from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def rubios_survey():

    def wait_for_new_url(driver, previous_url, timeout=5):
        def url_changed(driver):
            return driver.current_url != previous_url

        wait = WebDriverWait(driver, timeout)
        wait.until(url_changed)

    driver = webdriver.Chrome()
    driver.get("https://www.tellrubios.com/")
    
    current_url = driver.current_url
    wait = WebDriverWait(driver, 3)

    while not driver.current_url.startswith("https://www.tellrubios.com/Survey.aspx"):
        next_button = driver.find_element(by="id", value="NextButton")
        next_button.click()

        wait_for_new_url(driver, current_url)

    search_text = "Validation Code: "
    page_source = driver.page_source

    while search_text not in page_source:
        wait.until(EC.visibility_of_element_located((By.ID, "NextButton")))
        next_button = driver.find_element(by="id", value="NextButton")
        next_button.click()
        wait_for_new_url(driver, current_url)
        page_source = driver.page_source

    if driver.current_url.startswith("https://www.tellrubios.com/Finish.aspx"):
        text_elements = driver.find_element(By.XPATH, '//*[@id="finishIncentiveHolder"]/p[2]')
        validation_code = text_elements.text
        print("Success! - Rubio's")
        driver.quit()
        return validation_code
        
    input("Press Enter to close the browser...")
    driver.quit()

def main():
    valid_code = rubios_survey()
    print(valid_code)

if __name__ == "__main__":
    main()