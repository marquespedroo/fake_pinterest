from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt





app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///community.db"
app.config["SECRET_KEY"] = "5883be5d83e7049f8e6a2f9e7f66a700"
app.config["UPLOAD_FOLDER"] = "static/photos_posts"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

from fake_pinterest import routes