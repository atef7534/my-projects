from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from cs50 import SQL
import requests

app = Flask(__name__)

db = SQL("sqlite:///users.db")

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)

@app.route("/")
def index():
  if not session.get("user_id"):
    return render_template("login.html")
  return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
      return render_template("login.html")
    
    users = db.execute("SELECT * FROM users WHERE name = ? AND password = ?", username, password)
    if not users:
      return render_template("login.html")
    session["user_id"] = users[0]["id"]

    # ...
    return redirect("/")
  return render_template("login.html")


# logout system
@app.route("/logout")
def logout():
  session.clear()
  return redirect("/")

# registeration system
@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
      return render_template("register.html")
    
    allusers = db.execute("SELECT COUNT(*) AS C FROM users")
    db.execute("INSERT INTO users (id, name, password) VALUES (?, ?, ?)", int(allusers[0]["C"]) + 1, username, password)
    session["user_id"] = int(allusers[0]["C"]) + 1
    
    return redirect("/")
  return render_template("register.html")