from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.Post.forms import PostForm
from app import app, db
from app.models import Post

post_blueprint = Blueprint('Post',
                                __name__,
                                template_folder='templates/Post',
                                static_folder='static'
                                )

@post_blueprint.route("/new", methods=["GET","POST"])
@login_required
def new():
  form = PostForm()
  if form.validate_on_submit():
    post = Post(title=form.title.data, content=form.content.data, author=current_user)
    db.session.add(post)
    db.session.commit()
    flash('Your post has been created', 'success')
    return redirect(url_for('home'))
  return render_template('new.html', title='New Post', legend='New Post', form=form)


@post_blueprint.route("/<int:post_id>")
def get(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template('post.html',title=post.title, post=post)

@post_blueprint.route("/update/<int:post_id>", methods=["GET","POST"])
@login_required
def update(post_id):
  post = Post.query.get_or_404(post_id)

  # check author of post to check access
  if post.author != current_user:
    abort(403)

  form = PostForm()

  # if POST request
  if form.validate_on_submit():
    post.title      = form.title.data
    post.content    = form.content.data

    db.session.commit()
    flash('Your Post has been updated', 'success')
    return redirect(url_for('Post.get', post_id=post.id))

  elif request.method == "GET":
    form.title.data = post.title
    form.content.data = post.content

  return render_template('new.html', title='Update Post', legend='Update Post', form=form)

@post_blueprint.route("/delete/<int:post_id>", methods=["POST"])
@login_required
def delete(post_id):
  post = Post.query.get_or_404(post_id)
  # check author of post to check access
  if post.author != current_user:
    abort(403)
  
  db.session.delete(post)
  db.session.commit()

  flash('Your Post has been deleted', 'success')

  return redirect(url_for('home'))