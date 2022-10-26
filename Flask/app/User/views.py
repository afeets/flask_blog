from app import app, db, bcrypt, mail
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.User.forms import (LoginForm, RegistrationForm, UpdateAccountForm, 
  RequestPasswordResetForm, ResetPasswordForm)
from flask_mail import Message
from app.models import User, Post
import secrets
import os
from PIL import Image

user_blueprint = Blueprint('User',
                                __name__,
                                template_folder='templates/User',
                                static_folder='static'
                                )

@user_blueprint.route("/register", methods=["GET","POST"])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RegistrationForm()

  if form.validate_on_submit():
    
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(
      username = form.username.data, 
      email = form.email.data, 
      password = hashed_password
    )

    # Add user to Database
    db.session.add(user)
    db.session.commit()

    flash('Your account has been created. You can now log in.', 'success')
    return redirect(url_for('User.login')) 

  return render_template('register.html', title='Register', form=form)


@user_blueprint.route("/login", methods=["GET","POST"])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()
  if form.validate_on_submit():
    # attempt login
    # if form.email.data == 'admin@gmail.com' and form.password.data == 'password':
    #  flash('You have been logged in!', 'success')
    #  return redirect(url_for('home'))
    
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)

      # if previously redirected to the login page, 
      # look at next_page query string to define where to go now after completing login
      next_page = request.args.get('next') 
      return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
      flash('Login Unsuccessful. Please check Email and Password', 'danger')
  return render_template('login.html', title='Login', form=form)

@user_blueprint.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('home'))


def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  # get file extension
  _, f_ext = os.path.splitext(form_picture.filename)
  picture_filename = random_hex + f_ext
  
  # create path to directory string
  static_path = url_for('User.static', filename='profile_pics/' + picture_filename)
  full_path = app.root_path + static_path

  # resize picture
  output_size = (125,125)
  i = Image.open(form_picture)
  i.thumbnail(output_size)

  # save resized picture to newly file path
  i.save(full_path)

  return picture_filename

@user_blueprint.route("/account", methods=["GET","POST"])
@login_required
def account():
  form = UpdateAccountForm()
  if form.validate_on_submit():
    if form.picture.data:
      # call function to save picture and return filename
      picture_file = save_picture(form.picture.data)
      current_user.image_file = picture_file

    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Your account has been updated.','success')
    return redirect(url_for('User.account'))
  elif request.method == "GET":
    # populate form with current info
    form.username.data = current_user.username
    form.email.data = current_user.email
    

  image_file = url_for('User.static', filename='profile_pics/' + current_user.image_file)
  return render_template('account.html', title='Account', image_file=image_file, form=form)


@user_blueprint.route("/<string:username>")
def get_posts(username):
  page = request.args.get('page', 1, type=int)

  # get user, or return 404 if user not found
  user = User.query.filter_by(username=username).first_or_404()
  
  # paginate posts of user in descending time order
  posts = Post.query\
    .filter_by(author=user)\
    .order_by(Post.date_posted.desc())\
    .paginate(per_page=3, page = page)
  
  return render_template("posts.html", posts = posts, user=user)

# function to send email
def send_reset_email(user):
  token = user.get_reset_token()
  msg = Message('Password Reset Request', 
                sender='donotreply@gmail.com', 
                recipients=[user.email])
  
  # write message body
  msg.body = f'''To reset your password, visit the following link:
{ url_for('User.reset_password', token=token, _external=True) }

If you did not make this request, then ignore this email.
'''

  # send email  
  mail.send(msg)


@user_blueprint.route("/reset_request", methods=["GET","POST"])
def reset_request():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RequestPasswordResetForm()

  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    
    # call function to send reset password email
    send_reset_email(user)
    flash('An email has been sent with instructions to reset your password.', 'info')
    return redirect(url_for('User.login'))

  return render_template('reset_request.html', title='Reset Password', form=form)

# accept token to verify user
@user_blueprint.route('/reset_password/<string:token>', methods=["GET","POST"])
def reset_password(token):
  if current_user.is_authenticated:
    return redirect(url_for('home'))

  user = User.verify_reset_token(token)

  # return user id if found
  if user is None:
    flash('That is an invalid or expired token','warning')
    return redirect(url_for('reset_request'))

  form = ResetPasswordForm()

  if form.validate_on_submit():
    
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

    # Update and commit password in Database
    user.password = hashed_password
    db.session.commit()

    flash('Your password has been reset. You can now log in.', 'success')
    return redirect(url_for('User.login')) 



  return render_template('reset_password.html', title='Reset Password', form=form) 