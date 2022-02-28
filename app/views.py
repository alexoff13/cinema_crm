from flask import url_for, redirect, render_template, flash, g, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app
# from app.forms import ExampleForm, LoginForm
# from app.models import User


@app.route('/')
def index():
	return render_template('index.html')