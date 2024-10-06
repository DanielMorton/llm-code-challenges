import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class LanguageSelector:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def assign_language(self, programming_language):
        try:
            lang_select = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.text-sm.font-normal.group")))
            if programming_language.output_name.lower() not in lang_select.text.lower():
                lang_select.click()
                time.sleep(1)
                language_xpath = f"//div[contains(@class, 'text-text-primary') and text()='{programming_language.output_name}']"
                self.wait.until(EC.element_to_be_clickable((By.XPATH, language_xpath))).click()
            print(f"Successfully set language to {programming_language.output_name}.")
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error setting language to {programming_language.output_name}: {str(e)}")
            print("Attempting to continue with current language selection.")
