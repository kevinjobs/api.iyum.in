from . import db
from .base import BaseModel

class ImageModel(db.Model, BaseModel):
    __tablename__ = 'images'
    title = db.Column(db.String(80))
    author = db.Column(db.String(10))
    source = db.Column(db.String(100))
    desc = db.Column(db.Text)

    tags = db.Column(db.Text)
    category = db.Column(db.String(15))

    # location and the Latitude & Longitude
    location = db.Column(db.String(20))
    location_latitude = db.Column(db.Float(15))
    location_longitude = db.Column(db.Float(15))

    # the device of to take the photo
    device = db.Column(db.String(15))
    
    def __repr__(self):
        return '<标题: %r; 作者: %r>' % (self.title, self.author)