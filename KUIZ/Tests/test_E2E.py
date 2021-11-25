# import unittest
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
#
# class TestSelenium(unittest.TestCase):
#     """Tests of the Selenium E2E."""
#
#     def setUp(self):
#         """Set up an browser driver before each test."""
#         my_options = Options()
#         my_options.headless = True
#
#         assert my_options.headless
#
#         path_to_driver = ""  # Your PATH/TO/DRIVER
#         self.browser = webdriver.Chrome(path_to_driver, options=my_options)
#         self.browser.implicitly_wait(10)
#
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
#
#     def test_get_tile(self):
#         """Test that KUIZ in html Title"""
#         url = "https://ku-kuiz.herokuapp.com/kuiz/detail/"
#         self.browser.get(url)
#         self.assertIn("KUIZ", self.browser.title)
#
#     def test_user_require_login(self):
#         """Test user require to login before can customize the profile"""
#         elements = self.browser.find_elements_by_tag_name("a")
#         url_lists = []
#         for links in elements:
#             pages_index = links.get_attribute('href')
#             url_lists.append(pages_index)
#         profile_index = "https://ku-kuiz.herokuapp.com/user/profile/" in url_lists
#         self.assertFalse(profile_index)
#
#     def test_login(self):
#         username = "wasd1234"
#         password = "1234"
#         url = "https://ku-kuiz.herokuapp.com/user/login/"
#         self.browser.get(url)
#         username_box = self.browser.find_element_by_xpath('//*[@id="id_login"]')
#         username_box.send_keys(username)
#         password_box = self.browser.find_element_by_xpath('//*[@id="id_password"]')
#         password_box.send_keys(password)
#         self.browser.find_element_by_xpath('/html/body/div/div[1]/div/div/div/div[2]/form/div[3]/button').click()
#         self.assertIs(self.browser, webdriver)
