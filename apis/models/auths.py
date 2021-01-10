from . import db
from .base import BaseModel

class InvitationModel(db.Model, BaseModel):
    __tablename__ = 'invitations'
    code = db.Column(db.String(20))
    useable = db.Column(db.Integer)