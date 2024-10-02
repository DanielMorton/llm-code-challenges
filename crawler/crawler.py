import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class Crawler:
    def __init__(self):
        self.driver = uc.Chrome(use_subprocess=True)
        self.wait = WebDriverWait(self.driver, 30)
        print("Crawler initialized.")

    def navigate_to(self, url):
        self.driver.get(url)
        print(f"Navigated to {url}")

    def find_element(self, by, value):
        return self.wait.until(ec.presence_of_element_located((by, value)))

    def click_element(self, by, value):
        element = self.wait.until(ec.element_to_be_clickable((by, value)))
        element.click()
        print(f"Clicked element: {by}={value}")

    def input_text(self, by, value, text):
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)
        print(f"Input text into element: {by}={value}")

    def get_text(self, by, value):
        return self.find_element(by, value).text

    def current_url(self):
        return self.driver.current_url

    def press_keys(self, by, value, *keys):
        element = self.find_element(by, value)
        element.send_keys(keys)
        print(f"Pressed keys {keys} on element: {by}={value}")