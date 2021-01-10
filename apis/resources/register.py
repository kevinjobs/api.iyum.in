from flask import g, current_app
from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError

from models.user import UserModel, db
from models.auths import InvitationModel

from common import pretty_result, code
from app import hash_ids

class RegisterResource(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()

	def post(self):
		'''
		username & password get from request parser
		can be 
		1. json
		2. multipart/form-data
		3. application/x-www.form-urlencoded
		return: [dict] username & id & token
		'''
		self.parser.add_argument('username', type=str)
		self.parser.add_argument('password', type=str)
		self.parser.add_argument('invitation', type=str)
		args = self.parser.parse_args()

		try:
			invitation = InvitationModel.query.filter_by(code=args.invitation).first()
			if invitation:
				if not invitation.useable:
					return pretty_result(code.AUTHORIZATION_ERROR, '邀请码已经使用')
				# 邀请码只能使用一次; python 中 1 为 true
				invitation.useable = 0
				db.session.add(invitation)
			else:
				return pretty_result(code.AUTHORIZATION_ERROR, '邀请码不存在')
		except SQLAlchemyError as e:
			current_app.logger.error(e)
			db.session.rollback()
			return pretty_result(code.DB_ERROR, '数据库错误!')

		try:
			user = UserModel(username=args.username)
			user.hash_password(args.password) # hash密码 避免明文保存
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
