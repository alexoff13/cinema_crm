

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect


app = Flask(__name__)
app.config.from_object('app.config.Config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)
bc = Bcrypt(app)  # flask-bcrypt

lm = LoginManager()  # flask-loginmanager
lm.init_app(app)       # init the login manager


from app import views, models