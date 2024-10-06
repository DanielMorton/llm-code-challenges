import time

from selenium.webdriver.common.by import By


class LanguageSelector:
    def __init__(self, crawler):
        self.crawler = crawler

    def assign_language(self, programming_language):
        try:
            lang_select = self.crawler.wait_for_clickable_element(By.CSS_SELECTOR, "button.text-sm.font-normal.group")
            if programming_language.output_name.lower() not in lang_select.text.lower():
                lang_select.click()
                time.sleep(1)
                language_xpath = f"//div[contains(@class, 'text-text-primary') and text()='{programming_language.output_name}']"
                self.crawler.wait_for_clickable_element(By.XPATH, language_xpath).click()
            print(f"Successfully set language to {programming_language.output_name}.")
        except Exception as e:
            print(f"Error setting language to {programming_language.output_name}: {str(e)}")
            print("Attempting to continue with current language selection.")
