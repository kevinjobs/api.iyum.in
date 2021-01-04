from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.image import ImageModel, db
from sqlalchemy.exc import SQLAlchemyError

from .auth import Auth, auth
from app import hash_ids
from common import pretty_result, code

	
class ImageListResource(Resource, Auth):
	def __init__(self):
		self.parser = reqparse.RequestParser()

	@auth.login_required
	def post(self):
		self.parser.add_argument('create_time', type=str)
		# self.parser.add_argument('update_time', type=str)

		self.parser.add_argument('title', type=str)
		self.parser.add_argument('source', type=str)
		self.parser.add_argument('author', type=str)
		self.parser.add_argument('desc', type=str)

		self.parser.add_argument('tags', type=str)
		self.parser.add_argument('category', type=str)

		self.parser.add_argument('manufacturer', type=str)
		self.parser.add_argument('system_version', type=str)
		self.parser.add_argument('cameral_model', type=str)
		self.parser.add_argument('cameral_lens', type=str)

		self.parser.add_argument('exposure_time', type=str)
		self.parser.add_argument('iso', type=int)

		self.parser.add_argument('width', type=int)
		self.parser.add_argument('length', type=int)

		self.parser.add_argument('latitude', type=float)
		self.parser.add_argument('latitude_ref', type=str)
		self.parser.add_argument('longitude', type=float)
		self.parser.add_argument('longitude_ref', type=str)
		self.parser.add_argument('altitude', type=float)
		self.parser.add_argument('altitude_ref', type=str)

		self.parser.add_argument('position', type=str)
		
		args = self.parser.parse_args()

		image = ImageModel(
			create_time = args.create_time,
			# update_time = args.update_time,
			# 
			title = args.title,
			author = args.author,
			source = args.source,
			desc = args.desc,
			#
			tags = args.tags,
			category = args.category,
			#
			manufacturer = args.manufacturer,
			system_version = args.system_version,
			cameral_model = args.cameral_model,
			cameral_lens = args.cameral_lens,
			#
			exposure_time = args.exposure_time,
			iso = args.iso,
			#
			latitude = args.latitude,
			latitude_ref = args.latitude_ref,
			longitude = args.longitude,
			longitude_ref = args.longitude_ref,
			altitude = args.altitude,
			altitude_ref = args.altitude_ref,
			#
			position = args.position
		)

		try:
			db.session.add(image)
			db.session.commit()
		except SQLAlchemyError as e:
			current_app.logger.error(e)
			db.session.rollback()
			return pretty_result(code.DB_ERROR, '数据库错误!')
		else:
			return pretty_result(code.OK)

	def get(self):
		self.parser.add_argument('page', type=int, location='args', default=1)
		self.parser.add_argument('limit', type=int, location='args', default=9)

		# self.parser.add_argument('create_time', type=str)
		# self.parser.add_argument('update_time', type=str)

		# self.parser.add_argument('title', type=str)
		# self.parser.add_argument('source', type=str)
		self.parser.add_argument('author', type=str)
		# self.parser.add_argument('desc', type=str)

		# self.parser.add_argument('tags', type=str)
		self.parser.add_argument('category', type=str)

		# self.parser.add_argument('manufacturer', type=str)
		# self.parser.add_argument('system_version', type=str)
		# self.parser.add_argument('cameral_model', type=str)
		# self.parser.add_argument('cameral_lens', type=str)

		# self.parser.add_argument('exposure_time', type=str)
		# self.parser.add_argument('iso', type=int)

		# self.parser.add_argument('width', type=int)
		# self.parser.add_argument('length', type=int)

		# self.parser.add_argument('latitude', type=float)
		# self.parser.add_argument('latitude_ref', type=str)
		# self.parser.add_argument('longitude', type=float)
		# self.parser.add_argument('longitude_ref', type=str)
		# self.parser.add_argument('altitude', type=float)
		# self.parser.add_argument('altitude_ref', type=str)

		# self.parser.add_argument('position', type=str)
		args = self.parser.parse_args()

		filter_rules = []

		#if args.create_time:
		#	filter_rules.append(ImageModel.create_time == args.create_time)
		if args.author:
			filter_rules.append(ImageModel.author == args.author)
		if args.category:
			filter_rules.append(ImageModel.category == args.category)
		#if args.position:
		#	filter_rules.append(ImageModel.position == args.position)

		try:
			images = ImageModel.query.filter(*filter_rules).paginate(
				args.page,
				args.limit,
				error_out=False
			)
		except SQLAlchemyError as e:
			current_app.logger.error(e)
			db.session.rollback()
			return pretty_result(code.DB_ERROR, '数据库错误!')
		else:
			items = []
			for i in images.items:
				items.append(i.to_dict())
			data = {
				'page': args.page,
				'limit': args.limit,
				'total': images.total,
				'items': items
			}
			return pretty_result(code.OK, data=data)

	

class ImageResource(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()

	@staticmethod
	def get(id):
		id = hash_ids.decode(id)
		if not id: abort(404)

		try:
			image = ImageModel.query.get(id[0])
			next_a = ImageModel.query.get(id[0] + 1)
			prev_a = ImageModel.query.get(id[0] - 1)
			if not image: abort(404)
		except SQLAlchemyError as e:
			current_app.logger.error(e)
			db.session.rollback()
			return pretty_result(code.DB_ERROR, '数据库错误!')
		else:
			data = {
				'next': next_a.to_dict() if next_a else None,
				'prev': prev_a.to_dict() if prev_a else None,
				'current': image.to_dict()
			}
			return pretty_result(code.OK, data=data)

	@auth.login_required
	def put(self, id):
		self.parser.add_argument('title', type=str)
		self.parser.add_argument('source', type=str)
		self.parser.add_argument('author', type=str)
		self.parser.add_argument('desc', type=str)
		self.parser.add_argument('tags', type=str)
		self.parser.add_argument('category', type=str)
		self.parser.add_argument('location', type=str)
		self.parser.add_argument('device', type=str)
		args = self.parser.parse_args()

		id = hash_ids.decode(id)
		if not id: abort(404)

		try:
			image = ImageModel.query.get(id[0])
			if not image: abort(404)

			image.source = args.source if args.source else image.source
			image.title = args.title if args.title else image.title
			image.author = args.author if args.author else image.author
			image.desc = args.desc if args.desc else image.desc
			image.tags = args.tags if args.tags else image.tags
			image.category = args.category if args.category else image.category
			image.device = args.device if args.device else image.device
			image.location = args.location if args.location else image.location

			db.session.add(image)
			db.session.commit()
		except SQLAlchemyError as e:
			current_app.logger.error(e)
			db.session.rollback()
			return pretty_result(code.DB_ERROR, '数据库错误!')
		else:
			return pretty_result(code.OK)

	@staticmethod
	@auth.login_required
	def delete(id):
		id = hash_ids.decode(id)
		if not id: abort(404)

		try:
			image = ImageModel.query.get(id[0])
			if not image: abort(404)

			db.session.delete(image)
			db.session.commit()
		except SQLAlchemyError as e:
			current_app.logger.error(e)
			db.session.rollback()
			return pretty_result(code.DB_ERROR, '数据库错误！')
		else:
			return pretty_result(code.OK)