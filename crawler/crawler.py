import undetected_chromedriver as uc  # type: ignore

from selenium.webdriver.support.ui import WebDriverWait  # For waiting for elements to appear
from selenium.webdriver.support import expected_conditions as ec  # For defining expected conditions for WebDriverWait


class Crawler:
    def __init__(self):
        print("Initializing LeetCrawler.")
        self.driver = uc.Chrome(use_subprocess=True)  # Initialize a Chrome WebDriver instance
        self.wait = WebDriverWait(self.driver, 30)  # Create a WebDriverWait object with a 30-second timeout
        print("LeetCrawler initialized.")

    def navigate_to(self, url):
        print(f"Navigating to {url}")
        self.driver.get(url)  # Use the WebDriver to navigate to the specified URL
        print(f"Navigation complete.")

    def find_element(self, by, value):
        print(f"Finding element by {by}: {value}...")
        element = self.wait.until(
            ec.presence_of_element_located((by, value)))  # Wait for the element to be present in the DOM
        print("Element found.")
        return element

    def click_element(self, by, value):
        print(f"Clicking element by {by}: {value}...")
        element = self.wait.until(ec.element_to_be_clickable((by, value)))  # Wait for the element to be clickable
        element.click()  # Click the element
        print("Element clicked.")

    def input_text(self, by, value, text):
        print(f"Inputting text into element by {by}: {value}...")
        element = self.find_element(by, value)  # Find the input element
        element.clear()  # Clear any existing text in the element
        element.send_keys(text)  # Input the new text
        print("Text input complete.")

    def get_text(self, by, value):
        print(f"Getting text from element by {by}: {value}...")
        text = self.find_element(by, value).text  # Find the element and get its text content
        print(f"Text retrieved: {text}...")
        return text

    def current_url(self):
        url = self.driver.current_url  # Get the current URL from the WebDriver
        print(f"Current URL: {url}")
        return url

    def press_keys(self, by, value, *keys):
        print(f"Pressing keys {keys} on element by {by}: {value}...")
        element = self.find_element(by, value)  # Find the element to send keys to
        element.send_keys(keys)  # Send the specified keys to the element
        print("Keys pressed.")

