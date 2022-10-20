from app import app
from flask import render_template, request, url_for

@app.route("/")
@app.route("/home")
def home():
  return render_template("public/home.html")

@app.route("/about")
def about():
  return render_template("public/about.html")