from . import db
from .base import BaseModel
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from uuid import uuid4

class UserModel(db.Model, BaseModel):
    __tablename__ = 'users'
    uid = db.Column(db.String(50), default=str(uuid4()))
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.LargeBinary)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def generate_auth_token(self, expiration = 3600):
        s = Serializer('&JSPV@4i', expires_in = expiration) # 用于混淆
        return s.dumps({ 'id': self.id }) # 通过 id 来混淆

    @staticmethod
    def verify_auth_token(token):
        s = Serializer('secret')
        try:
            data = s.loads(token) # 从传入的 token 中解析
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = UserModel.query.get(data['id']) # 获取 id 对应的用户
        return user

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)