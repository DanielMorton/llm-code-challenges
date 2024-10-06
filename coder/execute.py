import logging
import time

from selenium.common import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By

from coder import RUN_BUTTON, SUBMIT_BUTTON


class CodeExecutor:
    def __init__(self, crawler):
        self.crawler = crawler

    def input_code(self, code):
        try:
            js_set_editor_value = f"monaco.editor.getEditors()[0].setValue(`{code}`);"
            self.crawler.execute_script(js_set_editor_value)
        except Exception as e:
            print(f"Error inputting code: {str(e)}")

    def run_code(self):
        try:
            run_button = self.crawler.find_element(By.CSS_SELECTOR, RUN_BUTTON)
            run_button.click()
        except (ElementClickInterceptedException, NoSuchElementException) as e:
            logging.warning(f"Could not click run button: {e}. Attempting keyboard shortcut.")
            try:
                self.crawler.press_key(By.CSS_SELECTOR, '.monaco-editor textarea', Keys.CONTROL, Keys.ENTER)
            except Exception as e:
                logging.error(f"Failed to run code using keyboard shortcut: {e}")
                raise
        except Exception as e:
            logging.error(f"Unexpected error when trying to run code: {e}")
            raise

    def submit_solution(self):
        try:
            self.crawler.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON).click()
            time.sleep(5)
        except Exception as e:
            print(f"Error submitting solution: {str(e)}")