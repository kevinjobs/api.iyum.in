import os

MODE = 'dev'


class DevelopConfig(object):
	HOST = '127.0.0.1'
	PORT = '5000'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///./example.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_ECHO = True
	DEBUG = True
	SECRET = 'impossible'
	TEMPLATE_FOLDER = 'templates'


if MODE == 'dev':
	config = DevelopConfig