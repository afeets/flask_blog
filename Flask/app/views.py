from app import app
from flask import render_template, request, url_for
from app.models import Post

# url home/?page=<int>
@app.route("/")
@app.route("/home")
def home():
  page = request.args.get('page', 1, type=int)
  # paginate posts in descending time order
  posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=3, page = page)
  return render_template("public/home.html", posts = posts)

@app.route("/about")
def about():
  return render_template("public/about.html")