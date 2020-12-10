from flask import g
from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError

from models.user import UserModel, db

from common import pretty_result, code
from app import hash_ids

class RegisterResource(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()

	def post(self):
		self.parser.add_argument('username', type=str)
		self.parser.add_argument('password', type=str)
		args = self.parser.parse_args()

		try:
			user = UserModel(username=args.username)
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
