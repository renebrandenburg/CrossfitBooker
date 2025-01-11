import unittest
from unittest.mock import MagicMock, patch
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

from scraping_script import init_driver, login, navigate_to_gym, navigate_to_schedule, scrape_schedule

class TestScrapingScript(unittest.TestCase):

    @patch('scraping_script.webdriver.Chrome')
    def test_init_driver(self, mock_chrome):
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        driver = init_driver(debug=False)

        self.assertEqual(driver, mock_driver)
        mock_chrome.assert_called_once()

    @patch('scraping_script.WebDriverWait')
    @patch('scraping_script.webdriver.Chrome')
    def test_login(self, mock_chrome, mock_wait):
        mock_driver = MagicMock(spec=WebDriver)
        mock_chrome.return_value = mock_driver
        mock_wait.return_value.until.return_value = True

        mock_username_elem = MagicMock(spec=WebElement)
        mock_password_elem = MagicMock(spec=WebElement)
        mock_code_elem = MagicMock(spec=WebElement)
        mock_btn_elem = MagicMock(spec=WebElement)
        mock_captcha_elem = MagicMock(spec=WebElement)

        # Mock CAPTCHA URL
        mock_captcha_elem.get_attribute.return_value = "https://example.com/captcha.png"

        # Return elements in the correct order
        mock_driver.find_element.side_effect = [
            mock_username_elem,
            mock_password_elem,
            mock_code_elem,
            mock_btn_elem,
            mock_captcha_elem,
        ]

        # Call the function
        login(mock_driver, "test_user", "test_pass", "1234")

        # Verify calls
        mock_username_elem.send_keys.assert_called_once_with("test_user")
        mock_password_elem.send_keys.assert_called_once_with("test_pass")
        mock_code_elem.send_keys.assert_called_once_with("1234")
        mock_btn_elem.click.assert_called_once()


    @patch('scraping_script.BeautifulSoup')
    @patch('scraping_script.webdriver.Chrome')
    def test_navigate_to_gym(self, mock_chrome, mock_bs4):
        mock_driver = MagicMock(spec=WebDriver)
        mock_chrome.return_value = mock_driver
        mock_bs4.return_value.find.return_value.get_text.return_value = "current_gym"

        navigate_to_gym(mock_driver, "desired_gym")

        mock_driver.find_element.assert_any_call(By.CLASS_NAME, "current-club-name")
        mock_driver.find_element.assert_any_call(By.XPATH, f"//a[text()='desired_gym']")

    @patch('scraping_script.WebDriverWait')
    @patch('scraping_script.webdriver.Chrome')
    def test_navigate_to_schedule(self, mock_chrome, mock_wait):
        mock_driver = MagicMock(spec=WebDriver)
        mock_chrome.return_value = mock_driver

        navigate_to_schedule(mock_driver)

        mock_wait.assert_called_once()

    @patch('scraping_script.BeautifulSoup')
    @patch('scraping_script.webdriver.Chrome')
    def test_scrape_schedule(self, mock_chrome, mock_bs4):
        mock_driver = MagicMock(spec=WebDriver)
        mock_chrome.return_value = mock_driver
        mock_schedule = MagicMock()
        mock_bs4.return_value.find.return_value = mock_schedule

        scrape_schedule(mock_driver)

        mock_bs4.assert_called_once_with(mock_driver.page_source, "html.parser")
        mock_schedule.prettify.assert_called_once()

if __name__ == '__main__':
    unittest.main()
