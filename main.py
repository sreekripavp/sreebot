from tasks.survey import open_survey
from tasks.attendance import check_attendance
from utils import save_credentials
from dotenv import load_dotenv
import os

# Load saved credentials
load_dotenv()

saved_user = os.getenv("PORTAL_USER")
saved_pass = os.getenv("PORTAL_PASS")

# Ask only if credentials already exist
if saved_user and saved_pass:

    print("\nSaved credentials found.")
    print("1) Continue with saved credentials")
    print("2) New User")

    choice = input("\nChoose option: ").strip()

    # Erase old credentials
    if choice == "2":

        save_credentials("", "")

        print("Old credentials removed.")
        print("New credentials will be asked automatically.")

while True:

    print("\n===== SREEBOT =====")
    print("1) Survey")
    print("2) Attendance")
    print("3) Exit")

    command = input("\nChoose an option: ").lower().strip()

    # Survey
    if command == "1" or command == "survey":
        open_survey()

    # Attendance
    elif command == "2" or command == "attendance":
        check_attendance()

    # Exit
    elif command == "3" or command == "exit":
        print("Goodbye!")
        break

    else:
        print("Unknown command")