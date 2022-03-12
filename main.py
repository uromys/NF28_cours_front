"""
A simple selenium test example written by python
"""
import os
from dotenv import load_dotenv
from parameterized import parameterized
import pickle
import shutil
load_dotenv()

import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




class TestTemplate(unittest.TestCase):
    """Include test cases on a given url"""

    def setUp(self):
        """Start web driver"""

        # used an entry point to do before each test
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument(r"user-data-dir=./chromedriverFolder/data")
        executable_path = "/home/anael/Documents/utc/NF28/testCour"
        chrome_options.add_argument(argument='--window-size=1366x768');
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        self.driver.implicitly_wait(7)
        self.login()
    def tearDown(self):
        """Stop web driver"""

        # method call when you are over


        self.driver.quit()



    def login(self):
        """logging to utc website"""
        try:
            anaelPassword = os.getenv('passwordAnael')
            self.driver.get('https://cas.utc.fr/cas/login?service=https%3A%2F%2Fwebapplis.utc.fr%2Fent%2Findex.jsf')
            passwordInput = self.driver.find_element_by_xpath("//input[contains(@id,'password')]")
            passwordInput.send_keys(anaelPassword)
            usernameInput = self.driver.find_element_by_xpath("//input[contains(@id,'username')]")
            usernameInput.send_keys("lacouran")
            buttonLogin = self.driver.find_element_by_name("Submit1")
            buttonLogin.click()

            pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        except NoSuchElementException as ex:
            self.fail(ex.msg)


    def pourquoi_je_suis_pas_lance(self):
        """navigate throught a specific page"""
        try:
            self.driver.get("https://webapplis.utc.fr/ent/services/services.jsf?sid=578")
        except NoSuchElementException as ex:
            self.fail(ex.msg)


    # @parameterized.expand([
    #     ["https://webapplis.utc.fr/ent/services/services.jsf?sid=578"],
    #     ["https://webapplis.utc.fr/ent/services/services.jsf?sid=599"]
    # ])
    # def test_navigate_to(self, url):
    #     """ navigate throught a specific page """
    #     try:
    #         self.driver.get(url)
    #         self.driver.find_element_by_id("MainBar")
    #     except NoSuchElementException as ex:
    #         self.fail(ex.msg)

    # def test_search_logic_baaad(self):
    #     try:
    #         searchForm=self.driver.find_element_by_id("mySearch:SearchEngine")
    #         searchForm.send_keys("moodle")
    #         loupeIcon=self.driver.find_element_by_id("mySearch:Search")
    #         loupeIcon.click()
    #         assert self.driver.current_url=="https://ngapplis.utc.fr/ent/ent?s=moodle"
    #         # exemple typique selenium qui ne retry pas, cypress aurait retry, du coup en code "Selenium cela donne"
    #
    #     except NoSuchElementException as ex:
    #         self.fail(ex.msg)

    def test_search_logic_good_pratice(self):

        try:
            wait = WebDriverWait(self.driver, 10)
            searchForm = self.driver.find_element_by_id("mySearch:SearchEngine")
            searchForm.send_keys("moodle")
            loupeIcon = self.driver.find_element_by_id("mySearch:Search")
            loupeIcon.click()
            wait.until(EC.url_to_be("https://ngapplis.utc.fr/ent/ent?s=moodle"))

        except NoSuchElementException as ex:
            self.fail(ex.msg)



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplate)
    unittest.TextTestRunner(verbosity=1).run(suite)
