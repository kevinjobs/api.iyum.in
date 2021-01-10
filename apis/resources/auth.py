from flask import g
from flask_httpauth import HTTPBasicAuth

from models.user import UserModel

auth = HTTPBasicAuth()

class Auth(object):
	
	@staticmethod
	@auth.verify_password
	def verify_password(username_or_token, password) -> bool:
		'''
		:params username_or_token: username with password, if token the password is not need.
		:params password: username with password
		:return: status of login
		'''
		user = UserModel.verify_auth_token(username_or_token)
		if not user:
			user = UserModel.query.filter_by(username=username_or_token).first()
			if not user or not user.verify_password(password):
				return False
		g.user = user
		return True
