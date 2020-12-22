from flask_restful import Resource, reqparse

from app import client
from common import pretty_result, code, transfer_objectid

class QuestionListResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=int)
        self.parser.add_argument('subject_id', type=int)
        #self.parser.add_argument('subject_name', type=str)
        self.parser.add_argument('chapter_id', type=int)
        #self.parser.add_argument('chapter_name', type=str)
        self.parser.add_argument('section_id', type=int)
        #self.parser.add_argument('section_name', type=str)
        self.args = self.parser.parse_args()

    def get(self):
        print(self.args)

        query = {'$and': []}
        if self.args.id:
            query['$and'].append({'id': self.args.id})
        if self.args.subject_id:
            query['$and'].append({'subject_id': self.args.subject_id})
        if self.args.chapter_id:
            query['$and'].append({'chapter_id': self.args.chapter_id})
        if self.args.section_id:
            query['$and'].append({'section_id': self.args.section_id})

        results = client.bodu.questions.find(query)
        questions = transfer_objectid(results)

        data = {
            'count': 3, #len(questions),
            'totals': client.bodu.questions.count(),
            'questions': questions
        }
        
        return pretty_result(code.OK, msg='成功获取到数据', data=data)


class QuestionResource(Resource):
    def __init__(self):
        pass

    @staticmethod
    def get(id):
        result = client.bodu.questions.find_one({'id': id})
        data = transfer_objectid(result)
        return pretty_result(code.OK, msg='成功获取到数据', data=data)
