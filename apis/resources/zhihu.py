from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.zhihu import ZhihuModel, db
from sqlalchemy.exc import SQLAlchemyError

from app import hash_ids
from common import pretty_result, code

class ZhihuListResource(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()

	@staticmethod
	def get():
		pass