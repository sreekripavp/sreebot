from flask import Flask, render_template, request, redirect, session
from tasks.survey import open_survey
from tasks.attendance import check_attendance
from utils import save_credentials
import os

app = Flask(__name__)
app.secret_key = "sreebot_secret"


# ---------- START PAGE ----------
@app.route("/")
def home():
    return render_template("start.html")


# ---------- CHOOSE OLD OR NEW ----------
@app.route("/choose", methods=["POST"])
def choose():

    choice = request.form.get("choice")

    if choice == "old":
        return redirect("/menu")

    elif choice == "new":
        return render_template("new_user.html")

    return redirect("/")


# ---------- SAVE NEW USER ----------
@app.route("/save-user", methods=["POST"])
def save_user():

    username = request.form.get("username")
    password = request.form.get("password")

    save_credentials(username, password)

    return redirect("/menu")


# ---------- MENU ----------
@app.route("/menu")
def menu():
    return render_template("menu.html")


# ---------- SURVEY ----------
@app.route("/survey")
def survey():
    open_survey()
    return "Survey completed. <br><a href='/menu'>Back</a>"


# ---------- ATTENDANCE ----------
@app.route("/attendance")
def attendance():

    data = check_attendance()

    html = "<h2>Attendance</h2>"

    for item in data:
        html += f"<p>{item['subject']} - {item['percent']}</p>"

    html += """
        <br>
        <h3>Do you want zone analysis?</h3>

        <a href="/zones"><button>Yes</button></a>
        <a href="/menu"><button>No</button></a>
    """

    return html


@app.route("/zones")
def zones():

    data = check_attendance()

    zones = {
        "DANGER ZONE": [],
        "RED ZONE": [],
        "GREEN ZONE": [],
        "ULTRA SAFE": []
    }

    for item in data:
        zones[item["zone"]].append(f"{item['subject']}: {item['percent']}")

    html = "<h2>Zone Analysis</h2>"

    for zone, items in zones.items():

        html += f"<h3>{zone}</h3>"

        if items:
            for i in items:
                html += f"<p>{i}</p>"
        else:
            html += "<p>None</p>"

    html += "<br><a href='/menu'><button>Back</button></a>"

    return html


import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))