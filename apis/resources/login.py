from flask import g
from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError

from .auth import auth, Auth
from models.user import UserModel, db

from common import pretty_result, code
from app import hash_ids

class LoginResource(Resource, Auth):
	def __init__(self):
		self.parser = reqparse.RequestParser()

	@auth.login_required
	def post(self):
		''' test the login status from the flask global G
		only by the BASIC AUTH way.
		return: [dict] username & id & token.
		'''
		token = g.user.generate_auth_token().decode('utf-8')
		data = {
			'username': g.user.username,
			'id': hash_ids.encode(g.user.id),
			'token': token
		}
		return pretty_result(code.OK, data=data)
