from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd119af253a2062ec517bd2c4887423fb'

# Configure SQLite DB
db_path = os.path.join(os.path.dirname(__file__), 'site.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'User.login'
login_manager.login_message_category = 'info'

from app import views

# Register Blueprints
from app.User.views import user_blueprint


app.register_blueprint(user_blueprint, url_prefix='/User')