import logging

import re
import time
from coder import (
    PROBLEM_DESCRIPTION, INNER_HTML, LEETCODE_PROBLEM_PREFIX
)
from coder.execute import CodeExecutor
from coder.language import LanguageSelector
from coder.navigator import ProblemNavigator
from coder.problem_parser import ProblemParser
from coder.result import ResultHandler
from crawler.leetcrawler import LeetCrawler
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class LeetCoder(LeetCrawler):
    def __init__(self, code_gen, programming_language, headless=False, max_attempts=3):
        super().__init__(headless=headless, max_attempts=max_attempts)
        self.code_gen = code_gen
        self.programming_language = programming_language
        self.problem_parser = ProblemParser()
        self.code_executor = CodeExecutor(self.driver, self.wait)
        self.result_handler = ResultHandler(self.driver, self.wait)
        self.problem_navigator = ProblemNavigator(self.driver, self.wait)
        self.language_selector = LanguageSelector(self.driver, self.wait)

    def get_problem_description(self):
        try:
            description_element = self.find_element(By.CSS_SELECTOR, PROBLEM_DESCRIPTION)
            html_content = description_element.get_attribute(INNER_HTML)
            return re.sub(r'\n\s*\n', '\n\n', self.problem_parser.parse_leetcode_problem(html_content)).strip()
        except Exception as e:
            logging.error(f"Error getting problem description: {str(e)}")
            return ""

    def get_starting_code(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.view-lines')))
            code_lines = self.driver.find_elements(By.CSS_SELECTOR, '.view-line')
            return '\n'.join(line.text for line in code_lines if line.text)
        except Exception as e:
            logging.error(f"Error getting starting code: {str(e)}")
            return ""

    def complete_individual_problem(self, problem_title):
        logging.info(f"Starting to solve problem: {problem_title}")
        if not self.get_current_url().startswith(LEETCODE_PROBLEM_PREFIX):
            raise ValueError("Not on a LeetCode problem page")

        problem_description = self.get_problem_description()
        starting_code = self.get_starting_code()
        logging.info(f"Problem description:\n{problem_description}")
        logging.info(f"Starting code:\n{starting_code}")

        for attempt in range(self.max_attempts):
            logging.info(f"Attempt {attempt + 1} of {self.max_attempts}")
            code = (self._generate_code(problem_description, starting_code) if attempt == 0
                    else self._handle_error(problem_description, code, starting_code, results['result'], error_info))
            logging.info(f"Code for attempt {attempt + 1}:\n{code}")
            self.code_executor.input_code(code)
            self.code_executor.run_code()
            time.sleep(5)
            results = self.result_handler.get_test_results()
            logging.info(f"Test Results:\n{results}")

            if results['result'] == "Accepted":
                logging.info("Problem solved successfully!")
                self.code_executor.submit_solution()
                return True
            elif results['result'] == "Runtime Error":
                error_info = f"Runtime Error:\n{results['error_message']}\nInput: {results['cases'][0]['Input']}"
            else:
                error_info = "\n".join(f"Case {i + 1}:\n" + "\n".join(f"{k}: {v}" for k, v in case.items())
                                       for i, case in enumerate(results['cases']))

        logging.warning(f"Max retries reached. Adding problem '{problem_title}' to failed list and moving to next problem.")
        return False

    def _generate_code(self, problem_description, starting_code):
        return self.code_gen.generate_code(problem_description, starting_code)

    def _handle_error(self, problem_description, current_code, starting_code, error_message, error_info):
        return self.code_gen.handle_error(problem_description, current_code, starting_code, error_message, error_info)