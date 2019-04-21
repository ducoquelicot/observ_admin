from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from elasticsearch import Elasticsearch

observ = Flask(__name__)
observ.config.from_object(Config)
db = SQLAlchemy(observ)
migrate = Migrate(observ, db)
login = LoginManager(observ)
login.login_view = 'login'
mail = Mail(observ)
es = Elasticsearch([observ.config['ELASTICSEARCH_URL']])

from app import routes, models, errors, search