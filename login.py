from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from utils import save_credentials
import os

load_dotenv()

PORTAL_URL = os.getenv("PORTAL_URL")


def login():

    load_dotenv(override=True)

    username = os.getenv("PORTAL_USER")
    password = os.getenv("PORTAL_PASS")

    # Ask only if missing (local fallback)
    if not username or not password:
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        save_credentials(username, password)

    playwright = sync_playwright().start()

    # ✅ CLOUD SAFE BROWSER (IMPORTANT FIX)
    browser = playwright.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox"
        ]
    )

    context = browser.new_context()
    page = context.new_page()

    page.goto(PORTAL_URL)

    # ✅ safer waits
    page.wait_for_selector("#LoginForm_username", timeout=15000)

    page.fill("#LoginForm_username", username)
    page.fill("#LoginForm_password", password)

    page.click('button[type="submit"]')

    # wait for navigation after login
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    # 🚨 CHECK LOGIN SUCCESS
    if "login" in page.url.lower():
        raise Exception("Login failed — still on login page")

    print("Login successful!")

    return page, context, playwright
