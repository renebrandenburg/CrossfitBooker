from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve sensitive variables
API_KEY = os.getenv("API_KEY")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
CONFIRM_CODE = os.getenv("CONFIRM_CODE")


PAGE_URL = "https://crossfitrijswijk.virtuagym.com/"
SITE_KEY = "6LfMFSkTAAAAACXKnvs3pxy2z-TO0478L7EEZuTZ"

def solve_recaptcha(api_key, site_key, page_url):
    """Solve Google reCAPTCHA using 2Captcha."""
    import requests
    import time

    response = requests.post(
        "http://2captcha.com/in.php",
        data={
            "key": api_key,
            "method": "userrecaptcha",
            "googlekey": site_key,
            "pageurl": page_url,
        }
    )
    if "OK" not in response.text:
        raise Exception(f"Error from 2Captcha: {response.text}")
    captcha_id = response.text.split("|")[1]

    # Poll for the solution
    solution = None
    while not solution:
        time.sleep(5)
        result = requests.get(f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}")
        if "OK" in result.text:
            solution = result.text.split("|")[1]

    return solution

def main():
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
