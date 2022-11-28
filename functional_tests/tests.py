import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        # self.browser = webdriver.Firefox()
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    # def check_for_row_in_list_table(self, row_text):
    #     table = self.browser.find_element(By.ID, 'id_list_table')
    #     rows = table.find_elements(By.TAG_NAME, 'tr')
    #     self.assertIn(row_text, [row.text for row in rows])

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)
        # self.browser.get('http://localhost:8000')
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)
        # self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)
        # self.check_for_row_in_list_table('1: Buy peacock feathers')
        # self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.fail('Finish the test!')

        # The page updates again, and now shows both items on her list
        # [...]

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        # Now a new user, Francis, comes along to the site.
        # We use a new browser session to make sure that no information
        # of Edith's is coming through from cookies etc
        self.browser.quit()
        # self.browser = webdriver.Firefox()
        self.browser = webdriver.Chrome()
        # Francis visits the home page. There is no sign of Edith's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)
        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)
        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
        # Satisfied, they both go back to sleep
