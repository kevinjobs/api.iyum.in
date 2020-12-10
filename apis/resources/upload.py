from flask import abort, current_app, g, request
from flask_restful import Resource, reqparse
from models.user import UserModel, db
from sqlalchemy.exc import SQLAlchemyError

from common import pretty_result, code
from app import hash_ids

class UploadAvatarResource(Resource):
	def post(self):
		file = request.files['file'].read()
		try:
			user = UserModel(avatar=file)
			
			db.session.add(user)
			db.session.commit()
		except SQLAlchemyError as e:
			current_app.logger.error(e)
			db.session.rollback()
			return pretty_result(code.DB_ERROR, '数据库错误!')
		else:
			return pretty_result(code.OK)

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