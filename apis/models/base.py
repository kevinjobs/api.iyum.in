import datetime
from . import db
from app import hash_ids

class BaseModel(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(
        db.String(20),
        default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    update_time = db.Column(
        db.String(20),
        default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        onupdate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    def to_dict(self):
        adict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        adict['id'] = hash_ids.encode(self.id)
        return adict
