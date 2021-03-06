import pymysql
from flask import Flask
from flask_login import LoginManager
from FlaskDemo import config
from FlaskDemo.exts import db

pymysql.install_as_MySQLdb()
import MySQLdb

login_manager = LoginManager()
login_manager.sessison_protection = 'strong'
login_manager.login_view = 'login'


app = Flask(__name__)

app.config.from_object(config)
db.init_app(app)
login_manager.init_app(app)
