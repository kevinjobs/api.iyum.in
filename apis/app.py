import string
from hashids import Hashids
from flask import Flask
from flask_cors import CORS
# from flask_pymongo import PyMongo

from models import db
from config import config

app = Flask(__name__)
app.config.from_object(config)

# anti cors
CORS(app)

# hash id
hash_ids = Hashids(salt='hvwptlmj129d5quf', min_length=8, alphabet=string.ascii_lowercase + string.digits)

def _access_control(response):
    """
    解决跨域请求
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,HEAD,PUT,PATCH,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Max-Age'] = 86400
    return response

def create_app():
    app.after_request(_access_control)
    db.init_app(app)
    from routes import v2
    app.register_blueprint(v2, url_prefix='/api/v2')
    return app