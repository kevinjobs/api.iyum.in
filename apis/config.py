import os
import datetime

MODE = 'dev'



class DevelopConfig(object):
	HOST = '127.0.0.1'
	PORT = '5000'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///./mint-forge-%s.db' % datetime.datetime.now().strftime('%Y%m%d')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_ECHO = True
	DEBUG = True
	SECRET = 'impossible'
	TEMPLATE_FOLDER = 'templates'
	MONGO_URI = 'mongodb://kevinjobs:SsAm7PHaIVMdq6EQ@cluster0-shard-00-00.6os1r.mongodb.net:27017,cluster0-shard-00-01.6os1r.mongodb.net:27017,cluster0-shard-00-02.6os1r.mongodb.net:27017/bodu?ssl=true&replicaSet=atlas-fd1sjd-shard-0&authSource=admin&retryWrites=true&w=majority'


class ProdConfig(object):
	HOST = '127.0.0.1'
	PORT = '5000'
	SQLALCHEMY_DATABASE_URI = 'sqlite:////home/iyum/iyumdb.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_ECHO = True
	DEBUG = False
	SECRET = 'impossible'
	TEMPLATE_FOLDER = 'templates'

if MODE == 'dev':
	config = DevelopConfig
elif MODE == 'prod':
	config = ProdConfig