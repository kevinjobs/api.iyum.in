from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.question import QuestionModel, db
from sqlalchemy.exc import SQLAlchemyError

from .auth import Auth, auth
from app import hash_ids
from common import pretty_result, code

    
class QuestionListResource(Resource, Auth):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    # @auth.login_required
    def post(self):
        self.parser.add_argument('ques_id', type=int)
        self.parser.add_argument('ques_type', type=int)
        self.parser.add_argument('ques_stem', type=str)
        self.parser.add_argument('ques_option', type=str)
        self.parser.add_argument('ques_right', type=str)
        self.parser.add_argument('ques_analysis', type=str)

        self.parser.add_argument('subject_id', type=int)
        self.parser.add_argument('chapter_id', type=int)
        self.parser.add_argument('section_id', type=int)
        self.parser.add_argument('subject_name', type=str)
        self.parser.add_argument('chapter_name', type=str)
        self.parser.add_argument('section_name', type=str)

        self.parser.add_argument('spent_time', type=str)
        self.parser.add_argument('do_datetime', type=str)
        self.parser.add_argument('right_times', type=int)
        self.parser.add_argument('starred', type=int)
        self.parser.add_argument('remark', type=str)

        args = self.parser.parse_args()

        question = QuestionModel(
            ques_id = args.ques_id,
            ques_type = args.ques_type,
            ques_stem = args.ques_stem,
            ques_option = args.ques_option,
            ques_right = args.ques_right,
            ques_analysis = args.ques_analysis,

            subject_id = args.subject_id,
            chapter_id = args.chapter_id,
            section_id = args.section_id,

            subject_name = args.subject_name,
            chapter_name = args.chapter_name,
            section_name = args.section_name,

            spent_time = args.spent_time,
            do_datetime = args.do_datetime,
            right_times = args.right_times,
            starred = args.starred,
            remark = args.remark
        )

        try:
            db.session.add(question)
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
        self.parser.add_argument('subject_id', type=int, location='args')
        self.parser.add_argument('chapter_id', type=int, location='args')
        self.parser.add_argument('section_id', type=int, location='args')
        self.parser.add_argument('ques_id', type=int, location='args')
        args = self.parser.parse_args()

        filter_rules = []

        if args.subject_id:
            filter_rules.append(QuestionModel.subject_id == args.subject_id)
        if args.chapter_id:
            filter_rules.append(QuestionModel.chapter_id == args.chapter_id)
        if args.section_id:
            filter_rules.append(QuestionModel.section_id == args.section_id)

        try:
            questions = QuestionModel.query.filter(*filter_rules).paginate(
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
            for i in questions.items:
                items.append(i.to_dict())
            data = {
                'page': args.page,
                'limit': args.limit,
                'total': questions.total,
                'items': items
            }
            return pretty_result(code.OK, data=data)
