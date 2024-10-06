import time

from selenium.webdriver.common.by import By

from coder import LEETCODEFILTER


class ProblemNavigator:
    def __init__(self, crawler):
        self.crawler = crawler

    def navigate_to_new_problem(self, df):
        current_page = 1
        while True:
            self.crawler.navigate_to(f"{LEETCODEFILTER}{current_page}")
            time.sleep(5)
            self.crawler.presence_of_element_located(By.CSS_SELECTOR, 'div[role="rowgroup"]')

            for row in self.crawler.find_elements(By.CSS_SELECTOR, 'div[role="row"]'):
                cells = row.find_elements(By.CSS_SELECTOR, 'div[role="cell"]')
                if len(cells) >= 2:
                    title_link = cells[1].find_element(By.CSS_SELECTOR, 'a[href^="/problems/"]')
                    if 'opacity-60' not in title_link.get_attribute('class') and title_link.text not in df[
                        'Problem Name']:
                        self.crawler.navigate_to(title_link.get_attribute('href'))
                        time.sleep(5)
                        return title_link.text

            next_button = self.crawler.find_element(By.XPATH, '//button[@aria-label="next"]')
            if next_button.is_enabled():
                next_button.click()
                current_page += 1
                time.sleep(5)
            else:
                break

        raise ValueError("No available problems found")