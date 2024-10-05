import random

from bs4 import BeautifulSoup
import re
import time
from selenium.common import NoSuchElementException, TimeoutException
from coder import (
    PROBLEM_DESCRIPTION, INNER_HTML, RUN_BUTTON, SUBMIT_BUTTON, RUNTIME_ERROR,
    TEST_CASE_BUTTON, TEST_CASE_INPUTS, TEST_CASE_OUTPUTS, LEETCODE_PROBLEM_PREFIX, LEETCODEFILTER, LEETCODEPOSTFILTER
)
from crawler.leetcrawler import LeetCrawler
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class LeetCoder(LeetCrawler):
    def __init__(self, max_retries, *args):
        super().__init__(*args)
        self.max_retries = max_retries

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

    def navigate_to_new_problem(self, current_page):
        print(f"Navigating to problem set page {current_page}...")
        self.navigate_to(
            f"{LEETCODEFILTER}{current_page}{LEETCODEPOSTFILTER}")  # Navigate to the problem set page

        while True:
            print(f"Waiting 5 seconds for problem list on page {current_page} to load...")
            time.sleep(5)

            print("Waiting for problem list to load...")
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'div[role="rowgroup"]'))
            )  # Wait for the problem list to load

            print("Selecting a random non-premium, non-failed problem...")
            problem_rows = self.driver.find_elements(By.CSS_SELECTOR,
                                                     'div[role="row"]')  # Find all problem rows
            available_problems = []

            for row in problem_rows:
                cells = row.find_elements(By.CSS_SELECTOR, 'div[role="cell"]')
                if len(cells) >= 2:
                    title_cell = cells[1]  # The title is in the second cell

                    # Check if the problem is not premium and not failed
                    title_link = title_cell.find_element(By.CSS_SELECTOR, 'a[href^="/problems/"]')
                    if 'opacity-60' not in title_link.get_attribute('class') and title_link.text not in FAILED_PROBLEMS:
                        available_problems.append(title_link)

            if available_problems:
                random_problem = random.choice(available_problems)  # Choose a random problem from available problems
                problem_url = random_problem.get_attribute('href')
                problem_title = random_problem.text
                print(f"Selected problem: {problem_title} from page {current_page}")
                print(f"Navigating to: {problem_url}")
                self.navigate_to(problem_url)  # Navigate to the selected problem
                print("Waiting 5 seconds for problem page to load...")
                time.sleep(5)  # Wait for 5 seconds after navigating to the problem
                return problem_title
            else:
                print(f"No available problems on page {current_page}. Attempting to go to next page...")
                next_button = self.driver.find_element(By.XPATH, '//button[@aria-label="next"]')
                if next_button.is_enabled():
                    next_button.click()  # Click the next page button if available
                    current_page += 1
                    print(f"Navigating to page {current_page}...")
                    time.sleep(5)  # Wait for 5 seconds after clicking next

        # Ensure Python language is selected
        self.ensure_python_language()

    def complete_individual_problem(self, code_gen, problem_title):
        print(f"Starting to solve problem: {problem_title}")
        current_url = self.current_url()
        if not current_url.startswith(LEETCODE_PROBLEM_PREFIX):
            print("Error: Not on a LeetCode problem page")
            raise ValueError("Not on a LeetCode problem page")

        # self.ensure_python_language()  # Make sure Python is selected as the programming language
        problem_description = self.get_problem_description()  # Get the problem description
        starting_code = self.get_starting_code()  # Get the initial code provided by LeetCode

        for attempt in range(self.max_retries):
            print(f"Attempt {attempt + 1} of {self.max_retries}")
            if not attempt:
                code = code_gen.generate_code(problem_description, starting_code)  # Generate initial code solution
            else:
                code = code_gen.handle_error(problem_description, code, starting_code, results['result'],
                                             error_info)  # Generate fixed code based on previous error
            print(f"Code for attempt {attempt + 1}:\n{code}")
            self.input_code(code)  # Input the generated code into LeetCode
            self.run_code()  # Run the code
            print("Waiting for test results...")
            time.sleep(5)  # Wait for results
            results = self.get_test_results()  # Get the test results

            print(f"Test Results:\n{results}")  # Print the full test results

            if results['result'] == "Accepted":
                print("Problem solved successfully!")
                self.submit_solution()  # Submit the solution if it's accepted
                return True
            elif results['result'] == "Runtime Error":
                print(f"Runtime Error encountered. Error message: {results['error_message']}")
                error_info = f"Runtime Error:\n{results['error_message']}\nInput: {results['cases'][0]['Input']}"
            else:
                print(f"Error encountered. Attempting to fix...")
                error_info = "\n".join(
                    [f"Case {i + 1}:\n" + "\n".join([f"{k}: {v}" for k, v in case.items()]) for i, case in
                     enumerate(results['cases'])])

        print(f"Max retries reached. Adding problem '{problem_title}' to failed list and moving to next problem.")
        # FAILED_PROBLEMS.add(problem_title)  # Add the problem to the failed problems set if max retries are reached
        return False
