"""
Scraping script to automate logging in, navigating, and scraping schedules using Playwright.
"""
import os
import time
import requests
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve sensitive variables
API_KEY = os.getenv("API_KEY")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
CONFIRM_CODE = os.getenv("CONFIRM_CODE")


PAGE_URL = "https://crossfitrijswijk.virtuagym.com/"
SITE_KEY = "6LfMFSkTAAAAACXKnvs3pxy2z-TO0478L7EEZuTZ"

def solve_recaptcha(api_key, site_key, page_url, max_retries=12):
    """Solve Google reCAPTCHA using 2Captcha.

    Args:
        api_key: 2Captcha API key.
        site_key: The site key for the reCAPTCHA widget.
        page_url: URL of the page containing the reCAPTCHA.
        max_retries: Maximum number of polling attempts while waiting for the
            captcha solution. Defaults to 12.
    """

    response = requests.post(
        "http://2captcha.com/in.php",
        timeout=10,
        data={
            "key": api_key,
            "method": "userrecaptcha",
            "googlekey": site_key,
            "pageurl": page_url,
        }
    )
    if "OK" not in response.text:
        raise ValueError(f"Error from 2Captcha: {response.text}")
    captcha_id = response.text.split("|")[1]

    # Poll for the solution
    retries = 0
    solution = None
    while not solution:
        if retries >= max_retries:
            raise TimeoutError("Exceeded maximum retries while solving reCAPTCHA")
        time.sleep(5)
        result = requests.get(
            f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}",
            timeout=10,
        )
        if "OK" in result.text:
            solution = result.text.split("|")[1]
        else:
            retries += 1

    return solution

def main():
    """
    Entry point for the script.

    Initializes the Playwright browser, performs the login process, 
    and handles scraping tasks.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Solve the reCAPTCHA
        print("Solving reCAPTCHA...")
        recaptcha_solution = solve_recaptcha(API_KEY, SITE_KEY, PAGE_URL)
        print(f"CAPTCHA solved: {recaptcha_solution}")

        # Perform login
        login(page, USERNAME, PASSWORD, CONFIRM_CODE, recaptcha_solution)

        browser.close()

def login(page, username, password, confirm_code, recaptcha_solution):
    """Login to the website."""
    page.goto(PAGE_URL)
    page.fill("#username", username)
    page.fill("#password", password)
    page.fill("#confirm_code", confirm_code)

    # Inject the CAPTCHA solution
    page.evaluate(f"""
        document.getElementById('g-recaptcha-response').value = '{recaptcha_solution}';
    """)
    page.click("#login_btn")

if __name__ == "__main__":
    main()
