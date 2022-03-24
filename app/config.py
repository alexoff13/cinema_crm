import os
from dotenv import load_dotenv
load_dotenv('.env')

class Config(object):
	"""
	Configuration base, for all environments.
	"""
	DEBUG = False
	TESTING = False
	SQLALCHEMY_DATABASE_URI = f'postgresql://{os.environ["POSTGRESS_USER"]}:{os.environ["POSTGRESS_PASS"]}@{os.environ["POSTGRESS_HOST"]}:5432/cinema'
	BOOTSTRAP_FONTAWESOME = True
	SECRET_KEY = "2x$e%!k_u_0*gq0s4!_u(2(^lpy&gir0hg)q&5nurj0-sseuav"
	CSRF_ENABLED = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True