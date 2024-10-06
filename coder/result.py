import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from coder import RUNTIME_ERROR, TEST_CASE_BUTTON, TEST_CASE_INPUTS, TEST_CASE_OUTPUTS


class ResultHandler:
    def __init__(self, crawler):
        self.crawler = crawler

    def get_test_results(self):
        try:
            result_or_error = self._wait_for_result_element()
            if "Runtime Error" in result_or_error.text:
                return self._handle_runtime_error(result_or_error)
            return self._process_test_cases(result_or_error)
        except TimeoutException:
            return {"result": "Timeout waiting for test results", "cases": []}
        except Exception as e:
            return {"result": f"Error: {str(e)}", "cases": []}

    def _wait_for_result_element(self):
        return self.crawler.presence_of_element_located(
            By.CSS_SELECTOR,
            'div[data-e2e-locator="console-result"], div.font-menlo.text-xs.text-red-60'
        )

    def _handle_runtime_error(self, result_or_error):
        input_elements = self.crawler.find_elements(By.XPATH, RUNTIME_ERROR)
        input_text = input_elements[0].text if input_elements else "Input not found"
        return {
            "result": "Runtime Error",
            "error_message": result_or_error.text,
            "cases": [{"Input": input_text}]
        }

    def _process_test_cases(self, result_or_error):
        result_text = result_or_error.text
        detailed_results = []
        for button in self.crawler.find_elements(By.CSS_SELECTOR, TEST_CASE_BUTTON):
            case_details = self._get_case_details(button)
            detailed_results.append(case_details)
        return {"result": result_text, "cases": detailed_results}

    def _get_case_details(self, button):
        button.click()
        time.sleep(1)
        case_details = {'Input': self.crawler.find_elements(By.XPATH, TEST_CASE_INPUTS)[0].text}
        for section in self.crawler.find_elements(By.CSS_SELECTOR, TEST_CASE_OUTPUTS):
            self._extract_section_details(section, case_details)
        return case_details

    @staticmethod
    def _extract_section_details(section, case_details):
        try:
            label = section.find_element(By.CSS_SELECTOR, 'div.text-xs.font-medium').text.strip()
            if label in ['Output', 'Expected']:
                case_details[label] = section.find_element(By.CSS_SELECTOR, 'div.font-menlo').text
        except NoSuchElementException:
            pass  # Silently skip elements that don't have the expected structure
