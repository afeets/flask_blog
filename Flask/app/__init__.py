from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail



import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')



# Configure SQLite DB
db_path = 'var/lib/sqlite/site.db'
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'User.login'
login_manager.login_message_category = 'info'


# config for email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('GMAIL_ADDRESS')
app.config['MAIL_PASSWORD'] = os.environ.get('GMAIL_PASSWORD')

mail = Mail(app)

from app import views

# Register Blueprints
from app.User.views import user_blueprint
from app.Post.views import post_blueprint
from app.Errors.handlers import errors_blueprint


app.register_blueprint(user_blueprint, url_prefix='/User')
app.register_blueprint(post_blueprint, url_prefix='/Post')
app.register_blueprint(errors_blueprint)
