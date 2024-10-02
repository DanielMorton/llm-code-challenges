from crawler import LEETCODE_LOGIN_URL, GOOGLE_LOGIN_BUTTON, CONTINUE_BUTTON, EMAIL, ANOTHER_AUTH, \
    PASSWORD, LEETCODE_URL, LEETCODE_PROBLEMSET_PREFIX, PROBLEM_LIST, ENTER_PW_BUTTON  # type: ignore
from crawler.crawler import Crawler

import time

from selenium.webdriver.common.by import By  # For locating elements on web pages
from selenium.webdriver.common.keys import Keys  # For simulating keyboard input
from selenium.webdriver.support import expected_conditions as ec  # For defining expected conditions for WebDriverWait
from selenium.common.exceptions import TimeoutException, \
    ElementClickInterceptedException  # For handling specific exceptions


class LeetCrawler(Crawler):

    def __init__(self, max_attempts=3):
        super().__init__()
        self.max_attempts = max_attempts

    def login(self, username, password):
        print("Attempting to log in.")
        self.navigate_to(LEETCODE_LOGIN_URL)  # Navigate to the LeetCode login page
        time.sleep(10)

        # Wait for the loading overlay to disappear
        try:
            self.wait.until(ec.invisibility_of_element_located((By.ID, "initial-loading")))
        except TimeoutException:
            print("Loading overlay did not disappear. Attempting to continue.")

        # Wait for and click Google login button
        for attempt in range(1, self.max_attempts + 1):
            try:
                google_login_button = self.wait.until(ec.element_to_be_clickable(
                    (By.CSS_SELECTOR, GOOGLE_LOGIN_BUTTON)))  # Wait for the GitHub login button to be clickable
                google_login_button.click()  # Click the GitHub login button
                break
            except (TimeoutException, ElementClickInterceptedException) as e:
                if attempt < self.max_attempts:
                    print(f"Attempt {attempt} failed. Retrying in 5 seconds.")
                    time.sleep(5)  # Wait for 5 seconds before retrying
                else:
                    print("Failed to click Google login button after multiple attempts.")
                    raise e

        # Wait for the "Continue" button on Google authorization page and click it
        print("Waiting for Continue button.")
        try:
            continue_button = self.wait.until(ec.element_to_be_clickable((By.XPATH,
                                                                          CONTINUE_BUTTON)))  # Wait for the Continue button to be clickable
            continue_button.click()  # Click the Continue button
            print("Clicked Continue button.")
        except TimeoutException:
            print("Continue button not found. Please check the page manually.")
            input("Press Enter after manually clicking Continue or if you need to proceed...")


        # Input username and password
        self.input_text(By.ID, EMAIL, username + Keys.ENTER)  # Enter the username
        try:
            another_auth_button = self.wait.until(
                ec.element_to_be_clickable((By.XPATH, ANOTHER_AUTH)))
            another_auth_button.click()
            print("Choose 'Try another way' authorization.")
        except TimeoutException:
            print("'Try another way' not found.")
            input("Press enter after manually clicking Continue.")
        try:
            another_auth_button = self.wait.until(ec.element_to_be_clickable((By.XPATH, ENTER_PW_BUTTON)))
            another_auth_button.click()
            print("Chose 'enter your password'. Move to password page.")
        except TimeoutException:
            print("Button not found.")
            input("Press enter after manually clicking 'enter your password'.")
        self.input_text(By.XPATH, PASSWORD,
                        password + Keys.ENTER)  # Enter the password

        # Wait for login to complete
        try:
            self.wait.until(ec.url_contains(LEETCODE_URL))  # Wait for the URL to change to LeetCode
            print("Login successful.")

            # Wait for 5 seconds after successful login
            print("Waiting 5 seconds after successful login...")
            time.sleep(5)

            # Navigate to the problems page
            print("Navigating to problems page...")
            leetcode_problemset = f"{LEETCODE_PROBLEMSET_PREFIX}1"
            self.navigate_to(leetcode_problemset)  # Navigate to the LeetCode problem set page

            # Wait for the problems page to load
            self.wait.until(ec.presence_of_element_located(
                (By.CSS_SELECTOR, PROBLEM_LIST)))  # Wait for the problem list to be present
            print("Successfully navigated to problems page.")

        except TimeoutException:
            print("Login failed. Please check your credentials.")