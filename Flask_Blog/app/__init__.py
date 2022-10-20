from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd119af253a2062ec517bd2c4887423fb'

from app import views

# Register Blueprints
from app.User.views import user_blueprint


app.register_blueprint(user_blueprint, url_prefix='/User')