from flask import Blueprint
from flask_restful import Api

from resources import articles, images, login, register, users

v2 = Blueprint('v2', __name__)

api = Api(v2)

api.add_resource(articles.ArticleListResource, '/articles')
api.add_resource(articles.ArticleResource, '/article/<string:id>')
api.add_resource(images.ImageListResource, '/images')
api.add_resource(images.ImageResource, '/image/<string:id>')

api.add_resource(login.LoginResource, '/login')
api.add_resource(register.RegisterResource, '/register')
api.add_resource(users.UserResource, '/user/<string:id>')
