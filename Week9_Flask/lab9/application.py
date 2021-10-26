import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":


        # Grab the form params; day, month, name.
        day = request.form.get("day")
        month = request.form.get("month")
        name = request.form.get("name")

        messages = []

        # Validate the name.
        if not name:
            messages.append("Name cannot be empty")

        # Validate the month.
        if not month:
            messages.append("Month cannot be empty")
        elif not 1 <= int(month) <= 12:
            messages.append("Invalid month value entered")

        # Validate the day.
        if not day:
            messages.append("Day cannot be empty")
        elif not 1 <= int(day) <= 31:
            messages.append("Invalid day value entered")

        # Insert the new birthday into the database.
        if len(messages) == 0:
            db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?,?)", name, month, day)
            birthdays = db.execute("SELECT * FROM birthdays")
            return render_template("index.html", birthdays=birthdays, messages=["Successfully registered"], color="green")
        else:
            return render_template("index.html", messages=messages, color="red")

    else:
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays)
