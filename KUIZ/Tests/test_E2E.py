# import unittest
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By

# class TestSelenium(unittest.TestCase):
#     """Tests of the Selenium E2E."""

#     def setUp(self):
#         """Set up an browser driver before each test."""
#         my_options = Options()
#         my_options.headless = True

#         assert my_options.headless

#         path_to_driver = "C:\\Users\\Acer\\Downloads\\chromedriver_win32\\chromedriver.exe"  # Your PATH/TO/DRIVER
#         self.browser = webdriver.Chrome(path_to_driver, options=my_options)
#         self.browser.implicitly_wait(10)

#     def test_access_to_KUIZ(self):
#         """Test that a Chrome driver can get url of KUIZ"""
#         url = "https://ku-kuiz.herokuapp.com/kuiz/"
#         self.browser.get(url)
#         self.assertEqual(url, self.browser.current_url)
#         url = "https://ku-kuiz.herokuapp.com/user/login/"
#         self.browser.get(url)
#         self.assertEqual(url, self.browser.current_url)
#         url = "https://ku-kuiz.herokuapp.com/kuiz/detail/chemistry"
#         self.browser.get(url)
#         self.assertEqual(url, self.browser.current_url)

#     def test_get_tile(self):
#         """Test title word in html Title"""
#         url = "https://ku-kuiz.herokuapp.com/kuiz/detail/"
#         self.browser.get(url)
#         self.assertIn("KUIZ", self.browser.title)
#         self.assertIn("All Quizzes", self.browser.title)

#     def test_user_require_login(self):
#         """Test user require to login before can customize the profile"""
#         elements = self.browser.find_elements_by_tag_name("a")
#         url_lists = []
#         for links in elements:
#             pages_index = links.get_attribute('href')
#             url_lists.append(pages_index)
#         profile_index = "https://ku-kuiz.herokuapp.com/user/profile/" in url_lists
#         self.assertFalse(profile_index)

#     def test_login(self):
#         """Test user login system with superuser"""
#         user = "wasd1234"
#         pwd = "1234"
#         url = "https://ku-kuiz.herokuapp.com/user/login/"
#         self.browser.get(url)
#         self.browser.find_element(By.NAME, 'username').send_keys(user)
#         self.browser.find_element(By.NAME, 'password').send_keys(pwd)
#         self.browser.find_element_by_xpath('//button[@type="submit"]').click()
#         self.assertNotEqual(url, self.browser.current_url)
