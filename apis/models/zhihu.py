from . import db
from .base import BaseModel

class ZhihuModel(db.Model, BaseModel):
	__tablename__ = 'zhihu_images'
	question_id = db.Column(db.Integer(16))
	question_title = db.Column(db.String(50))
	author_id = db.Column(db.Integer(16))
	author_name = db.Column(db.String(20))
