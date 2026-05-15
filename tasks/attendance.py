from login import login
import re


def get_zone(att):

    try:
        att = float(str(att).replace("%", "").strip())
    except:
        return "INVALID"

    if att < 75:
        return "DANGER ZONE"
    elif att < 80:
        return "RED ZONE"
    elif att < 85:
        return "GREEN ZONE"
    else:
        return "ULTRA SAFE"


def extract_percentage(text):

    match = re.search(r"(\d+(\.\d+)?)\s*%", text)
    if match:
        return match.group(1) + "%"
    return None


def check_attendance():

    page, context, playwright = login()

    try:
        page.goto("https://christ.etlab.app/user")

        page.wait_for_timeout(2000)

        page.click('a[href="/student/attendance"]')
        page.wait_for_timeout(2000)

        page.click('a[href*="viewattendancesubject"]')
        page.wait_for_timeout(3000)

        headers = page.locator("thead th").all_inner_texts()
        values = page.locator("tbody tr:first-child td").all_inner_texts()

        attendance = []

        for subject, raw in zip(headers[1:], values[1:]):

            if subject.lower() in ["roll no", "name", "total", "percentage"]:
                continue

            percent = extract_percentage(raw)
            if not percent:
                continue

            zone = get_zone(percent)

            attendance.append({
                "subject": subject,
                "percent": percent,
                "zone": zone
            })

        return attendance

    finally:
        context.close()
        playwright.stop()
