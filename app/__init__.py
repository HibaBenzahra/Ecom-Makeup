from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from app.db_models import db

app = Flask(__name__)


app.config["SECRET_KEY"] = '53478f9056dfa5900d5c153f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

#with app.app_context():
#	db.create_all()

from app import routes