import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Crawler:
    def __init__(self, headless=False, timeout=30):
        options = uc.ChromeOptions()
        options.headless = headless
        self.driver = uc.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, timeout)

    def navigate_to(self, url):
        """Navigate to the given URL."""
        self.driver.get(url)

    def find_element(self, by, value):
        """Find an element using Selenium expected_conditions."""
        return self.wait.until(ec.presence_of_element_located((by, value)))

    def click_element(self, by, value):
        """Click an element."""
        element = self.find_element(by, value)
        element.click()

    def input_text(self, by, value, text):
        """Input text into an appropriate element."""
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)

    def get_text(self, by, value):
        """Get text from an element."""
        element = self.find_element(by, value)
        return element.text

    def get_current_url(self):
        """Return the current URL."""
        return self.driver.current_url

    def press_key(self, by, value, *keys):
        """Press one or more Selenium keys on an element."""
        element = self.find_element(by, value)
        element.send_keys(*keys)

    def close(self):
        """Close the browser and end the session."""
        self.driver.quit()

    def wait_for_clickable_element(self, by, value):
        """Wait for an element to be clickable and return it."""
        return self.wait.until(ec.element_to_be_clickable((by, value)))

    def wait_for_presence_of_element(self, by, value):
        """Wait for an element to be present in the DOM and return it."""
        return self.wait.until(ec.presence_of_element_located((by, value)))
