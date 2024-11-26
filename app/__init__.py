from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from app.db_models import db
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)

app.config["SECRET_KEY"] = '53478f9056dfa5900d5c153f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ------- email configuration ----------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # for gmail
app.config['MAIL_USERNAME'] = 'benzahra.hiba@gmail.com'
app.config['MAIL_PASSWORD'] = 'b u k a o b w w c e a h t u p s'  # my own app password
app.config['MAIL_PORT'] = 587  # Use 465 for SSL or 587 for TLS
app.config['MAIL_USE_TLS'] = True  # Enable TLS encryption
app.config['MAIL_USE_SSL'] = False  # Set to True if you're using SSL instead of TLS

Bootstrap(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail(app)
s = URLSafeTimedSerializer(app.config["SECRET_KEY"])

from app import routes