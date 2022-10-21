from app import app, db, bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.User.forms import LoginForm, RegistrationForm, UpdateAccountForm
from app.models import User
import secrets
import os

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

  # save picture to newly file path
  form_picture.save(full_path)

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
