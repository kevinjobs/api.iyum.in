from flask import g, abort
from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError

from .auth import auth, Auth
from models.user import UserModel, db

from common import pretty_result, code
from app import hash_ids

class UserResource(Resource, Auth):
	'''
	对单个用户的改、查、删
	'''
	def __init__(self):
		self.parser = reqparse.RequestParser()

	@auth.login_required
	def put(self):
		self.parser.add_argument('username', type=str)
		self.parser.add_argument('password', type=str)
		args = self.parser.parse_args()

		id = g.user.id
		if not id: abort(404)

		try:
			user = UserModel.query.get(id)
			user.username = args.username
			user.hash_password(args.password)

			db.session.add(user)
			db.session.commit()
		except SQLAlchemyError as e:
			current_app.logger.error(e)
			db.session.rollback()
			return pretty_result(code.DB_ERROR, '数据库错误!')
		else:
			token = user.generate_auth_token().decode('utf-8')
			data = {
				'username': user.username,
				'id': hash_ids.encode(user.id),
				'token': token
			}
			return pretty_result(code.OK, data=data)
	
	@staticmethod
	@auth.login_required
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
	
	@staticmethod
	@auth.login_required
	def delete(id):
		id = hash_ids.decode(id)
		if not id: abort(404)

		try:
			user = UserModel.query.get(id[0])
			db.session.delete(user)
			db.session.commit()
		except SQLAlchemyError as e:
			current_app.logger.error(e)
			db.session.rollback()
			return pretty_result(code.DB_ERROR, '数据库错误!')
		else:
			data = {
				'id': hash_ids.encode(id[0]),
				'result': 1
			}
			return pretty_result(code.OK, data=data)
