from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from utils import save_credentials
import os

load_dotenv()

PORTAL_URL = os.getenv("PORTAL_URL")

def login():

    # Reload latest .env values
    load_dotenv(override=True)

    username = os.getenv("PORTAL_USER")
    password = os.getenv("PORTAL_PASS")

    # Ask only first time
    if not username or not password:

        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        save_credentials(username, password)

        print("Credentials saved successfully!")

    playwright = sync_playwright().start()

    context = playwright.chromium.launch_persistent_context(
        user_data_dir="playwright_profile",
        channel="chrome",
        headless=False,
        slow_mo=500
    )

    page = context.new_page()

    page.goto(PORTAL_URL)

    page.wait_for_load_state("domcontentloaded")
    page.wait_for_selector("#LoginForm_username", timeout=10000)

    page.wait_for_selector("#LoginForm_username")

    page.fill("#LoginForm_username", username)
    page.fill("#LoginForm_password", password)

    page.click('button[type="submit"]')

    page.wait_for_load_state("networkidle")

    print("Login successful!")

    return page, context, playwright