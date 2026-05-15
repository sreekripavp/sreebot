from login import login
from time import sleep
import random

def open_survey():

    page, context, playwright = login()

    try:
        page.goto("https://christ.etlab.app/survey/user/viewall")

        print("Survey bot started...")

        page.wait_for_timeout(3000)

        while True:

            survey_btn = page.locator("text=Do the Survey")

            if survey_btn.count() == 0:
                print("All surveys completed.")
                break

            survey_btn.first.click()

            page.wait_for_timeout(3000)

            answer_divs = page.locator("div.answer")
            count = answer_divs.count()

            for i in range(count):

                radios = answer_divs.nth(i).locator('input[type="radio"]')
                radio_count = radios.count()

                if radio_count > 0:

                    weights = [0.2, 0.45, 0.3, 0.05]

                    r = random.random()
                    total = 0
                    idx = 0

                    for j, w in enumerate(weights):
                        total += w
                        if r <= total:
                            idx = j
                            break

                    if idx >= radio_count:
                        idx = radio_count - 1

                    radios.nth(idx).check()

            print("Answers selected.")

            submit_btn = page.locator("text=Submit")

            if submit_btn.count() > 0:
                submit_btn.first.click()

            page.wait_for_timeout(3000)

        return "Survey completed successfully"

    finally:
        context.close()
        playwright.stop()
