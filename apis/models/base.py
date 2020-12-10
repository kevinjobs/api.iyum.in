import datetime
from . import db
from app import hash_ids

class BaseModel(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(
        db.DATETIME(6),
        default=datetime.datetime.now
    )
    update_time = db.Column(
        db.DATETIME(6),
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now
    )

    def to_dict(self):
        adict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        adict['id'] = hash_ids.encode(self.id)
        return adict
