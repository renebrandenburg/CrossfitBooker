import unittest
from unittest.mock import MagicMock, patch
from scraping_script import solve_recaptcha, login

class TestScrapingScript(unittest.TestCase):

    @patch('scraping_script.requests.post')
    @patch('scraping_script.requests.get')
    def test_solve_recaptcha(self, mock_get, mock_post):
        """Test solving reCAPTCHA using 2Captcha."""
        mock_post.return_value.text = "OK|123456789"
        mock_get.side_effect = [
            MagicMock(text="CAPTCHA_NOT_READY"),
            MagicMock(text="OK|solution-token")
        ]

        solution = solve_recaptcha("dummy_api_key", "dummy_site_key", "https://example.com")
        self.assertEqual(solution, "solution-token")
        mock_post.assert_called_once()
        mock_get.assert_called()

    @patch('scraping_script.requests.post')
    @patch('scraping_script.requests.get')
    def test_solve_recaptcha_retry_limit(self, mock_get, mock_post):
        """Ensure an error is raised after exceeding max_retries."""
        mock_post.return_value.text = "OK|123456789"
        mock_get.return_value.text = "CAPTCHA_NOT_READY"

        with self.assertRaises(TimeoutError):
            solve_recaptcha(
                "dummy_api_key",
                "dummy_site_key",
                "https://example.com",
                max_retries=3,
            )

        self.assertEqual(mock_get.call_count, 3)

    @patch('scraping_script.sync_playwright')
    def test_login(self, mock_playwright):
        """Test login functionality with Playwright."""
        mock_context = MagicMock()
        mock_page = MagicMock()
        mock_browser = MagicMock()
        mock_playwright.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        mock_page.goto.return_value = None
        mock_page.fill.return_value = None
        mock_page.click.return_value = None

        # Call the login function
        login(mock_page, "test_user", "test_pass", "1234", "recaptcha_solution")

        # Assert the interactions with the Playwright page
        mock_page.goto.assert_called_with("https://crossfitrijswijk.virtuagym.com/")
        mock_page.fill.assert_any_call("#username", "test_user")
        mock_page.fill.assert_any_call("#password", "test_pass")
        mock_page.fill.assert_any_call("#confirm_code", "1234")

        # Normalize and compare the evaluate call
        expected_script = (
            "document.getElementById('g-recaptcha-response').value = 'recaptcha_solution';"
        )
        actual_call_args = mock_page.evaluate.call_args[0][0].strip()
        self.assertEqual(expected_script.strip(), actual_call_args)

        mock_page.click.assert_called_with("#login_btn")

if __name__ == "__main__":
    unittest.main()

