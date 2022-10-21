from app import app
from flask import render_template, request, url_for
from app.models import Post


@app.route("/")
@app.route("/home")
def home():
  posts = Post.query.all()
  return render_template("public/home.html", posts = posts)

@app.route("/about")
def about():
  return render_template("public/about.html")