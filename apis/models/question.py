from . import db
from .base import BaseModel

class QuestionModel(db.Model, BaseModel):
    __tablename__ = 'questions'
    ques_id = db.Column(db.Integer, default=0)
    ques_type = db.Column(db.Integer, default=0)
    ques_stem = db.Column(db.Text, default='')
    ques_option = db.Column(db.Text, default='')
    ques_right = db.Column(db.String(10), default='')
    ques_analysis = db.Column(db.Text, default='')

    subject_id = db.Column(db.Integer, default=0)
    chapter_id = db.Column(db.Integer, default=0)
    section_id = db.Column(db.Integer, default=0)

    subject_name = db.Column(db.String(50), default='')
    chapter_name = db.Column(db.String(50), default='')
    section_name = db.Column(db.String(50), default='')

    spent_time = db.Column(db.String(100), default='')
    do_datetime = db.Column(db.String(200), default='')
    right_times = db.Column(db.Integer, default=0)
    starred = db.Column(db.Integer, default=0)
    remark = db.Column(db.Text, default='')
    
    def __repr__(self):
        return '<标题: %r; 作者: %r>' % (self.title, self.author)