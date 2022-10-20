from app import app
from flask import Blueprint, render_template, redirect, url_for, flash
from app.User.forms import LoginForm, RegistrationForm

user_blueprint = Blueprint('User',
                                __name__,
                                template_folder='templates/User')

@user_blueprint.route("/register", methods=["GET","POST"])
def register():
  form = RegistrationForm()

  if form.validate_on_submit():
    flash(f'Account created for { form.username.data }!', 'success')
    return redirect(url_for('home')) 

  return render_template('register.html', title='Register', form=form)


@user_blueprint.route("/login", methods=["GET","POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    # attempt login
    if form.email.data == 'admin@gmail.com' and form.password.data == 'password':
      flash('You have been logged in!', 'success')
      return redirect(url_for('home'))
    else:
      flash('Login Unsuccessful. Please check Username and Password', 'danger')
  return render_template('login.html', title='Login', form=form)