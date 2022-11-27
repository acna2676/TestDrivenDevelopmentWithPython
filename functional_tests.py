
# import unittest

# from selenium import webdriver


# class NewVisitorTest(unittest.TestCase):
#     def setUp(self):
#         # self.browser = webdriver.Firefox()
#         self.browser = webdriver.Chrome()

#     def tearDown(self):
#         self.browser.quit()

#     def test_can_start_a_list_and_retrieve_it_later(self):
#         # Edith has heard about a cool new online to-do app. She goes
#         # to check out its homepage
#         self.browser.get('http://localhost:8000')
#         # She notices the page title and header mention to-do lists
#         self.assertIn('To-Do', self.browser.title)
#         self.fail('Finish the test!')

#         # She is invited to enter a to-do item straight away
#         # [...rest of comments as before]
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')

import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        # self.browser = webdriver.Firefox()
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.fail('Finish the test!')

        # The page updates again, and now shows both items on her list
        # [...]
if __name__ == '__main__':
    unittest.main(warnings='ignore')
