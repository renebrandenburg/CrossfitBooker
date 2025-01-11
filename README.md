# Web Scraping Script

This project automates the process of logging in to a website, navigating to a specific gym schedule, and scraping the schedule data using Playwright.

## Features
- Automated login with CAPTCHA support
- Gym navigation and schedule retrieval
- Modular design for scalability
- Unit tests for robust validation

## Prerequisites
Ensure the following are installed on your system:
- Python 3.7 or higher
- Node.js (for Playwright dependencies)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/web-scraping-script.git
   cd web-scraping-script
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Install Playwright browsers:
   ```bash
   playwright install
   ```

## Usage
1. Update the configuration in `scraping_script.py`:
   - `BASE_URL`: URL of the target website
   - `BOOKING_GYM`: Name of the desired gym
   - Provide your login credentials in the `.env` file (see below).

2. Create a `.env` file in the project root:
   ```plaintext
   API_KEY=your_2captcha_api_key
   USERNAME=your_username
   PASSWORD=your_password
   CONFIRM_CODE=your_code
   ```

3. Run the script:
   ```bash
   python scraping_script.py
   ```

4. CAPTCHA Handling:
   - If using manual CAPTCHA solving, follow the instructions in the terminal.
   - If using an automated CAPTCHA service (e.g., 2Captcha), ensure your API key is set in the `.env` file.

## Project Structure
```
project/
├── scraping_script.py      # Main script
├── tests/                  # Unit tests
│   ├── __init__.py         # Marks the directory as a package
│   ├── test_scraping_script.py  # Test suite
├── requirements.txt        # Dependencies
├── .env                    # Environment variables (excluded from version control)
├── README.md               # Project documentation
```

## Running Tests
1. Activate the virtual environment (if not already active):
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```

2. Run the tests:
   ```bash
   python -m unittest discover -s tests
   ```

3. Use the verbose flag for more detailed output:
   ```bash
   python -m unittest discover -s tests -v
   ```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

