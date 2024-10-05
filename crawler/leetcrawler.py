from crawler import (
    LEETCODE_LOGIN_URL, GOOGLE_LOGIN_BUTTON, CONTINUE_BUTTON, EMAIL, ANOTHER_AUTH,
    PASSWORD, LEETCODE_URL, LEETCODE_PROBLEMSET_PREFIX, PROBLEM_LIST, ENTER_PW_BUTTON
)
from crawler.crawler import Crawler
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


class LeetCrawler(Crawler):
    def __init__(self, max_attempts=3, headless=False, timeout=30):
        super().__init__(headless=headless, timeout=timeout)
        self.max_attempts = max_attempts

    def login(self, username, password):
        print("Attempting to log in...")
        self.navigate_to(LEETCODE_LOGIN_URL)
        time.sleep(10)

        self._wait_for_loading_overlay()
        self._click_google_login_button()
        self._click_continue_button()
        self._enter_credentials(username, password)
        self._verify_login()

    def _wait_for_loading_overlay(self):
        try:
            self.wait.until(ec.invisibility_of_element_located((By.ID, "initial-loading")))
        except TimeoutException:
            print("Loading overlay did not disappear. Attempting to continue.")

    def _click_google_login_button(self):
        for attempt in range(1, self.max_attempts + 1):
            try:
                google_login_button = self.wait.until(
                    ec.element_to_be_clickable((By.CSS_SELECTOR, GOOGLE_LOGIN_BUTTON)))
                google_login_button.click()
                break
            except (TimeoutException, ElementClickInterceptedException) as e:
                if attempt < self.max_attempts:
                    print(f"Attempt {attempt} failed. Retrying in 5 seconds.")
                    time.sleep(5)
                else:
                    print("Failed to click Google login button after multiple attempts.")
                    raise e

    def _click_continue_button(self):
        try:
            continue_button = self.wait.until(ec.element_to_be_clickable((By.XPATH, CONTINUE_BUTTON)))
            continue_button.click()
            print("Clicked Continue button.")
        except TimeoutException:
            print("Continue button not found. Please check the page manually.")
            input("Press Enter after manually clicking Continue or if you need to proceed...")

    def _enter_credentials(self, username, password):
        self.input_text((By.ID, EMAIL), username + Keys.ENTER)
        self._handle_additional_auth()
        self.input_text((By.XPATH, PASSWORD), password + Keys.ENTER)

    def _handle_additional_auth(self):
        try:
            another_auth_button = self.wait.until(ec.element_to_be_clickable((By.XPATH, ANOTHER_AUTH)))
            another_auth_button.click()
            print("Chose 'Try another way' authorization.")
        except TimeoutException:
            print("'Try another way' not found.")
            input("Press enter after manually clicking Continue.")

        try:
            enter_pw_button = self.wait.until(ec.element_to_be_clickable((By.XPATH, ENTER_PW_BUTTON)))
            enter_pw_button.click()
            print("Chose 'enter your password'. Moving to password page.")
        except TimeoutException:
            print("'Enter your password' button not found.")
            input("Press enter after manually clicking 'enter your password'.")

    def _verify_login(self):
        try:
            self.wait.until(ec.url_contains(LEETCODE_URL))
            print("Login successful.")
            time.sleep(5)

            self.navigate_to(f"{LEETCODE_PROBLEMSET_PREFIX}1")

            self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, PROBLEM_LIST)))
            print("Successfully navigated to problems page.")
        except TimeoutException:
            print("Login failed. Please check your credentials.")