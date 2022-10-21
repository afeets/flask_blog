from flask import Blueprint, render_template, request, redirect, url_for, flash
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
  return render_template('new.html', title='New Post', form=form)