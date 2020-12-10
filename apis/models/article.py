from . import db
from .base import BaseModel

class ArticleModel(db.Model, BaseModel):
    __tablename__ = 'articles'
    cover = db.Column(db.Text)
    title = db.Column(db.String(80))
    author = db.Column(db.String(10))
    content = db.Column(db.Text)

    tags = db.Column(db.Text)
    category = db.Column(db.String(15))
    
    def __repr__(self):
        return '<文章标题: %r; 作者: %r>' % (self.title, self.author)