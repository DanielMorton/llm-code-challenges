from bs4 import BeautifulSoup  # type: ignore # For parsing HTML content
import re
import time

from selenium.common import NoSuchElementException, TimeoutException

from coder import PROBLEM_DESCRIPTION, INNER_HTML, RUN_BUTTON, SUBMIT_BUTTON, RUNTIME_ERROR, TEST_CASE_BUTTON, \
    TEST_CASE_INPUTS, TEST_CASE_OUTPUTS
from crawler.leetcrawler import LeetCrawler

from selenium.webdriver.common.by import By  # For locating elements on web pages
from selenium.webdriver.common.keys import Keys  # For simulating keyboard input
from selenium.webdriver.support import expected_conditions as ec


class LeetCoder(LeetCrawler):
    def __init__(self, *args):
        super().__init__(*args)

    @staticmethod
    def parse_leetcode_problem(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        def convert_formatting(element):
            if element.name == 'sup':
                return '^' + element.text
            elif element.name == 'sub':
                return '_' + element.text
            elif element.name == 'strong' or element.name == 'b':
                return f'**{convert_formatting_recursive(element)}**'
            elif element.name == 'em' or element.name == 'i':
                return f'*{convert_formatting_recursive(element)}*'
            elif element.name == 'code':
                return f'`{convert_formatting_recursive(element)}`'
            elif element.string:
                return element.string
            else:
                return convert_formatting_recursive(element)

        def convert_formatting_recursive(element):
            return ''.join(convert_formatting(child) for child in element.children)

        # Extract problem description
        description = convert_formatting_recursive(soup.find('p'))

        # Extract conditions
        conditions = [
            convert_formatting_recursive(li)
            for li in soup.find('ul').find_all('li')
        ]

        # Extract examples
        examples = []
        for example in soup.find_all('pre'):
            input_text = example.find('strong', string='Input:').next_sibling.strip()
            output_text = example.find('strong', string='Output:').next_sibling.strip()
            examples.append(f"Input: {input_text}\nOutput: {output_text}")

        # Extract constraints
        constraints = [
            convert_formatting_recursive(li)
            for li in soup.find_all('ul')[-1].find_all('li')
        ]

        # Construct the multiline string output
        output = f"""Description:
    {description}

    Conditions:
    {chr(10).join('- ' + condition for condition in conditions)}

    Examples:
    {chr(10).join(examples)}

    Constraints:
    {chr(10).join('- ' + constraint for constraint in constraints)}
    """

        return output

    def get_problem_description(self):
        print("Getting problem description...")
        try:
            # Get the HTML content of the description
            description_element = self.find_element(By.CSS_SELECTOR,
                                                    PROBLEM_DESCRIPTION)
            html_content = description_element.get_attribute(INNER_HTML)  # Get the HTML content of the description

            # Parse the HTML
            soup = BeautifulSoup(html_content, 'html.parser')  # Create a BeautifulSoup object to parse the HTML

            # Process the entire soup
            processed_text = self.parse_leetcode_problem(soup)

            # Remove extra newlines and spaces
            processed_text = re.sub(r'\n\s*\n', '\n\n', processed_text).strip()  # Clean up the processed text

            print(f"Problem description retrieved: {processed_text}...")
            return processed_text
        except Exception as e:
            print(f"Error getting problem description: {str(e)}")
            return ""

    def get_starting_code(self):
        print("Getting starting code...")
        try:
            # Wait for 5 seconds before attempting to get the starting code
            time.sleep(5)
            # Wait for the Monaco editor to load
            self.wait.until(ec.presence_of_element_located(
                (By.CSS_SELECTOR, '.view-lines')))  # Wait for the code editor to be present

            # Get all lines of code
            code_lines = self.driver.find_elements(By.CSS_SELECTOR,
                                                   '.view-line')  # Find all lines of code in the editor

            # Combine all lines into a single string
            code = '\n'.join([line.text for line in code_lines if line.text])  # Join all non-empty lines of code

            print(f"Starting code retrieved: {code}...")
            return code
        except Exception as e:
            print(f"Error getting starting code: {str(e)}")
            return ""

    def clear_code_editor(self):
        print("Clearing code editor...")
        try:
            # Use JavaScript to clear the editor
            js_clear_editor = """
            var editor = monaco.editor.getEditors()[0];
            editor.setValue('');
            """
            self.driver.execute_script(js_clear_editor)  # Execute JavaScript to clear the editor
            print("Code editor cleared.")
        except Exception as e:
            print(f"Error clearing code editor: {str(e)}")

    def input_code(self, code):
        print("Inputting code into editor...")
        self.clear_code_editor()  # Clear the existing code in the editor
        try:
            # Use JavaScript to set the value of the editor
            js_set_editor_value = f"""
            var editor = monaco.editor.getEditors()[0];
            editor.setValue(`{code}`);
            """
            self.driver.execute_script(js_set_editor_value)  # Execute JavaScript to set the new code in the editor
            print("Code input complete.")
        except Exception as e:
            print(f"Error inputting code: {str(e)}")

    def run_code(self):
        print("Running code...")
        try:
            # Find and click the "Run" button
            run_button = self.find_element(By.CSS_SELECTOR,
                                           RUN_BUTTON)  # Find the Run button
            run_button.click()  # Click the Run button
            print("Code execution initiated.")
        except Exception as e:
            print(f"Error running code: {str(e)}")
            # Fallback to keyboard shortcut if button not found
            self.press_keys(By.CSS_SELECTOR, '.monaco-editor textarea', Keys.CONTROL,
                            Keys.ENTER)  # Use keyboard shortcut to run code

    def get_test_results(self):
        print("Getting test results...")
        try:
            # Wait for either the test result or runtime error
            result_or_error = self.wait.until(ec.presence_of_element_located((
                By.CSS_SELECTOR,
                'div[data-e2e-locator="console-result"], div.font-menlo.text-xs.text-red-60'
            )))  # Wait for either the test result or error message to appear

            if "Runtime Error" in result_or_error.text:
                # Handle runtime error
                error_message = result_or_error.text
                input_elements = self.driver.find_elements(By.XPATH,
                                                           RUNTIME_ERROR)
                input_text = input_elements[0].text if input_elements else "Input not found"

                full_results = {
                    "result": "Runtime Error",
                    "error_message": error_message,
                    "cases": [{"Input": input_text}]
                }
            else:
                # Handle normal test results (existing code)
                result_text = result_or_error.text
                detailed_results = []
                case_buttons = self.driver.find_elements(By.CSS_SELECTOR,
                                                         TEST_CASE_BUTTON)  # Find all test case buttons

                for button in case_buttons:
                    button.click()  # Click each test case button
                    time.sleep(1)  # Wait for the case details to load

                    case_details = {}

                    # Find Input section
                    input_elements = self.driver.find_elements(By.XPATH,
                                                               TEST_CASE_INPUTS)
                    if input_elements:
                        case_details['Input'] = input_elements[0].text

                    # Find Output and Expected sections
                    sections = self.driver.find_elements(By.CSS_SELECTOR,
                                                         TEST_CASE_OUTPUTS)

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

                full_results = {
                    "result": result_text,
                    "cases": detailed_results
                }

            print(f"Test results retrieved: {full_results}")
            return full_results
        except TimeoutException:
            print("Timeout waiting for test results")
            return {"result": "Timeout waiting for test results", "cases": []}
        except Exception as e:
            print(f"An error occurred while getting test results: {str(e)}")
            return {"result": f"Error: {str(e)}", "cases": []}

    def submit_solution(self):
        print("Submitting solution...")
        try:
            submit_button = self.find_element(By.CSS_SELECTOR,
                                              SUBMIT_BUTTON)  # Find the Submit button
            submit_button.click()  # Click the Submit button
            print("Solution submitted successfully.")
            time.sleep(5)  # Wait for submit sleep
            print("Sleeping for 5 seconds after submit.")
        except Exception as e:
            print(f"Error submitting solution: {str(e)}")
