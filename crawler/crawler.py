import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Crawler:
    def __init__(self, headless=False, timeout=30):
        #options = uc.ChromeOptions()
        #options.headless = headless
        self.driver = uc.Chrome()
        self.wait = WebDriverWait(self.driver, timeout)

    def navigate_to(self, url):
        """Navigate to the given URL."""
        self.driver.get(url)

    def find_element(self, locator):
        """Find an element using Selenium expected_conditions."""
        return self.wait.until(ec.presence_of_element_located(locator))

    def click_element(self, locator):
        """Click an element."""
        element = self.find_element(locator)
        element.click()

    def input_text(self, locator, text):
        """Input text into an appropriate element."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Get text from an element."""
        element = self.find_element(locator)
        return element.text

    def get_current_url(self):
        """Return the current URL."""
        return self.driver.current_url

    def press_key(self, locator, *keys):
        """Press one or more Selenium keys on an element."""
        element = self.find_element(locator)
        element.send_keys(*keys)

    def close(self):
        """Close the browser and end the session."""
        self.driver.quit()
