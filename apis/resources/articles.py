from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.article import ArticleModel, db
from sqlalchemy.exc import SQLAlchemyError

from .auth import Auth, auth
from app import hash_ids
from common import pretty_result, code

	
class ArticleListResource(Resource, Auth):
	def __init__(self):
		self.parser = reqparse.RequestParser()

	@auth.login_required
	def post(self):
		self.parser.add_argument('cover', type=str)
		self.parser.add_argument('title', type=str)
		self.parser.add_argument('author', type=str)
		self.parser.add_argument('content', type=str)
		self.parser.add_argument('tags', type=str)
		self.parser.add_argument('category', type=str)
		args = self.parser.parse_args()

		article = ArticleModel(
			cover = args.cover,
			title = args.title,
			author = args.author,
			content = args.content,
			tags = args.tags,
			category = args.category
		)

		try:
			db.session.add(article)
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
		args = self.parser.parse_args()

		try:
			articles = ArticleModel.query.paginate(
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
			for i in articles.items:
				items.append(i.to_dict())
			data = {
				'page': args.page,
				'limit': args.limit,
				'total': articles.total,
				'items': items
			}
			return pretty_result(code.OK, data=data)


class ArticleResource(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()

	@staticmethod
	def get(id):
		id = hash_ids.decode(id)
		if not id: abort(404)

		try:
			article = ArticleModel.query.get(id[0])
			next_a = ArticleModel.query.get(id[0] + 1)
			prev_a = ArticleModel.query.get(id[0] - 1)
			if not article: abort(404)
		except SQLAlchemyError as e:
			current_app.logger.error(e)
			db.session.rollback()
			return pretty_result(code.DB_ERROR, '数据库错误!')
		else:
			data = {
				'next': next_a.to_dict() if next_a else None,
				'prev': prev_a.to_dict() if prev_a else None,
				'current': article.to_dict()
			}
			return pretty_result(code.OK, data=data)

	@auth.login_required
	def put(self, id):
		self.parser.add_argument('id', type=str)
		self.parser.add_argument('cover', type=str)
		self.parser.add_argument('title', type=str)
		self.parser.add_argument('author', type=str)
		self.parser.add_argument('content', type=str)
		self.parser.add_argument('tags', type=str)
		self.parser.add_argument('category', type=str)
		args = self.parser.parse_args()

		id = hash_ids.decode(id)
		if not id: abort(404)

		try:
			article = ArticleModel.query.get(id[0])
			if not article: abort(404)

			article.cover = args.cover
			article.title = args.title
			article.author = args.author
			article.content = args.content
			article.tags = args.tags
			article.category = args.category

			db.session.add(article)
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
			article = ArticleModel.query.get(id[0])
			if not article: abort(404)

			db.session.delete(article)
			db.session.commit()
		except SQLAlchemyError as e:
			current_app.logger.error(e)
			db.session.rollback()
			return pretty_result(code.DB_ERROR, '数据库错误！')
		else:
			return pretty_result(code.OK)