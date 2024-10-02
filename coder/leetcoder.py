from bs4 import BeautifulSoup
import re
import time
from selenium.common import NoSuchElementException, TimeoutException
from coder import (
    PROBLEM_DESCRIPTION, INNER_HTML, RUN_BUTTON, SUBMIT_BUTTON, RUNTIME_ERROR,
    TEST_CASE_BUTTON, TEST_CASE_INPUTS, TEST_CASE_OUTPUTS
)
from crawler.leetcrawler import LeetCrawler
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec


class LeetCoder(LeetCrawler):
    def __init__(self, *args):
        super().__init__(*args)

    @staticmethod
    def parse_leetcode_problem(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        def convert_formatting(element):
            if element.name in ['sup', 'sub']:
                prefix = '^' if element.name == 'sup' else '_'
                return prefix + element.text
            elif element.name in ['strong', 'b', 'em', 'i', 'code']:
                wrapper = '**' if element.name in ['strong', 'b'] else '*' if element.name in ['em', 'i'] else '`'
                return f"{wrapper}{convert_formatting_recursive(element)}{wrapper}"
            elif element.string:
                return element.string
            else:
                return convert_formatting_recursive(element)

        def convert_formatting_recursive(element):
            return ''.join(convert_formatting(child) for child in element.children)

        description = convert_formatting_recursive(soup.find('p'))
        conditions = [convert_formatting_recursive(li) for li in soup.find('ul').find_all('li')]
        examples = [f"Input: {example.find('strong', string='Input:').next_sibling.strip()}\n"
                    f"Output: {example.find('strong', string='Output:').next_sibling.strip()}"
                    for example in soup.find_all('pre')]
        constraints = [convert_formatting_recursive(li) for li in soup.find_all('ul')[-1].find_all('li')]

        return f"""Description:
{description}

Conditions:
{chr(10).join('- ' + condition for condition in conditions)}

Examples:
{chr(10).join(examples)}

Constraints:
{chr(10).join('- ' + constraint for constraint in constraints)}
"""

    def get_problem_description(self):
        try:
            description_element = self.find_element(By.CSS_SELECTOR, PROBLEM_DESCRIPTION)
            html_content = description_element.get_attribute(INNER_HTML)
            processed_text = self.parse_leetcode_problem(html_content)
            return re.sub(r'\n\s*\n', '\n\n', processed_text).strip()
        except Exception as e:
            print(f"Error getting problem description: {str(e)}")
            return ""

    def get_starting_code(self):
        try:
            time.sleep(5)
            self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.view-lines')))
            code_lines = self.driver.find_elements(By.CSS_SELECTOR, '.view-line')
            return '\n'.join([line.text for line in code_lines if line.text])
        except Exception as e:
            print(f"Error getting starting code: {str(e)}")
            return ""

    def clear_code_editor(self):
        try:
            js_clear_editor = "monaco.editor.getEditors()[0].setValue('');"
            self.driver.execute_script(js_clear_editor)
        except Exception as e:
            print(f"Error clearing code editor: {str(e)}")

    def input_code(self, code):
        self.clear_code_editor()
        try:
            js_set_editor_value = f"monaco.editor.getEditors()[0].setValue(`{code}`);"
            self.driver.execute_script(js_set_editor_value)
        except Exception as e:
            print(f"Error inputting code: {str(e)}")

    def run_code(self):
        try:
            run_button = self.find_element(By.CSS_SELECTOR, RUN_BUTTON)
            run_button.click()
        except Exception:
            self.press_keys(By.CSS_SELECTOR, '.monaco-editor textarea', Keys.CONTROL, Keys.ENTER)

    def get_test_results(self):
        try:
            result_or_error = self.wait.until(ec.presence_of_element_located((
                By.CSS_SELECTOR,
                'div[data-e2e-locator="console-result"], div.font-menlo.text-xs.text-red-60'
            )))

            if "Runtime Error" in result_or_error.text:
                input_elements = self.driver.find_elements(By.XPATH, RUNTIME_ERROR)
                input_text = input_elements[0].text if input_elements else "Input not found"
                return {
                    "result": "Runtime Error",
                    "error_message": result_or_error.text,
                    "cases": [{"Input": input_text}]
                }
            else:
                result_text = result_or_error.text
                detailed_results = []
                case_buttons = self.driver.find_elements(By.CSS_SELECTOR, TEST_CASE_BUTTON)

                for button in case_buttons:
                    button.click()
                    time.sleep(1)
                    case_details = {}

                    input_elements = self.driver.find_elements(By.XPATH, TEST_CASE_INPUTS)
                    if input_elements:
                        case_details['Input'] = input_elements[0].text

                    sections = self.driver.find_elements(By.CSS_SELECTOR, TEST_CASE_OUTPUTS)
                    for section in sections:
                        try:
                            label = section.find_element(By.CSS_SELECTOR, 'div.text-xs.font-medium').text.strip()
                            if label in ['Output', 'Expected']:
                                content = section.find_element(By.CSS_SELECTOR, 'div.font-menlo').text
                                case_details[label] = content
                        except NoSuchElementException:
                            continue

                    if case_details:
                        detailed_results.append(case_details)

                return {
                    "result": result_text,
                    "cases": detailed_results
                }
        except TimeoutException:
            return {"result": "Timeout waiting for test results", "cases": []}
        except Exception as e:
            return {"result": f"Error: {str(e)}", "cases": []}

    def submit_solution(self):
        try:
            submit_button = self.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON)
            submit_button.click()
            time.sleep(5)
        except Exception as e:
            print(f"Error submitting solution: {str(e)}")