from flask import Flask, render_template, redirect, url_for, session, abort
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
import os

# LOAD ENVIRONMENT VARIABLES

from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "blackdot-development-key"
)

DATABASE_URL = os.environ.get("DATABASE_URL")

FILMS = ["born-free", "emanzini"]

OPTIONS = ["loved", "good", "notforme"]


# DATABASE CONNECTION

def get_db():

    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is missing. Check your .env file."
        )

    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )


# GET VOTES

def get_votes(film):

    conn = get_db()

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT option, count FROM votes WHERE film = %s",
            (film,)
        )

        results = cursor.fetchall()

        votes = {
            "loved": 0,
            "good": 0,
            "notforme": 0
        }

        for row in results:
            votes[row["option"]] = row["count"]

        return votes

    finally:
        conn.close()


# PREPARE POLL DATA

def prepare_poll(film):

    votes = get_votes(film)

    total = sum(votes.values())

    if total == 0:
        loved_percent = 0
        good_percent = 0
        notforme_percent = 0

    else:
        loved_percent = round(votes["loved"] / total * 100)
        good_percent = round(votes["good"] / total * 100)
        notforme_percent = round(votes["notforme"] / total * 100)

    return {
        "loved": loved_percent,
        "good": good_percent,
        "notforme": notforme_percent,
        "loved_votes": votes["loved"],
        "good_votes": votes["good"],
        "notforme_votes": votes["notforme"],
        "total_votes": total,
        "has_voted": session.get(f"voted_{film}", False)
    }


# BLACKDOT HOMEPAGE

@app.route("/")
def home():

    return render_template("index.html")


# BORN FREE PAGE

@app.route("/born-free")
def born_free():

    poll = prepare_poll("born-free")

    return render_template(
        "born-free.html",
        **poll
    )


# EMANZINI PAGE

@app.route("/emanzini")
def emanzini():

    poll = prepare_poll("emanzini")

    return render_template(
        "emanzini.html",
        **poll
    )


# ABOUT PAGE

@app.route("/about")
def about():

    return render_template("about.html")


# CONTACT SECTION

@app.route("/contact")
def contact():

    return redirect(url_for("home") + "#contact")


# VOTING SYSTEM

@app.route("/vote/<film>/<option>", methods=["POST"])
def vote(film, option):

    if film not in FILMS or option not in OPTIONS:
        abort(404)

    if session.get(f"voted_{film}"):
        return redirect(url_for(film.replace("-", "_")))

    conn = get_db()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE votes
            SET count = count + 1
            WHERE film = %s AND option = %s
            """,
            (film, option)
        )

        conn.commit()

    finally:
        conn.close()

    session[f"voted_{film}"] = True

    return redirect(url_for(film.replace("-", "_")))


if __name__ == "__main__":
    app.run(debug=True)