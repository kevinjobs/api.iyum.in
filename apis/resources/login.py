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
		token = g.user.generate_auth_token().decode('utf-8')
		data = {
			'username': g.user.username,
			'id': hash_ids.encode(g.user.id),
			'token': token
		}
		return pretty_result(code.OK, data=data)
	
	@staticmethod
	def get(id):
		id = hash_ids.decode(id)
		if not id: abort(404)

		try:
			user = UserModel.query.get(id[0])
		except SQLAlchemyError as e:
			current_app.logger.error(e)
			db.session.rollback()
			return pretty_result(code.DB_ERROR, '数据库错误!')
		else:
			data = {
				'id': hash_ids.encode(user.id),
				'username': user.username,
				'avatar': user.avatar
			}
			return pretty_result(code.OK, data=data)
