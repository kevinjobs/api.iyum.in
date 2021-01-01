from . import db
from .base import BaseModel

class ImageModel(db.Model, BaseModel):
    __tablename__ = 'images'
    title = db.Column(db.String(80), default="")
    author = db.Column(db.String(10), default="")
    source = db.Column(db.String(100), default="")
    desc = db.Column(db.Text, default="")

    tags = db.Column(db.Text, default="")
    category = db.Column(db.String(15), default="")

    # the exif
    manufacturer = db.Column(db.String(20), default="")
    system_version = db.Column(db.String(20), default="")
    cameral_model = db.Column(db.String(20), default="")
    cameral_lens = db.Column(db.String(30), default="")

    exposure_time = db.Column(db.String(10), default="")
    iso = db.Column(db.Integer, default=0)

    width = db.Column(db.Integer, default=0)
    length = db.Column(db.Integer, default=0)

    latitude = db.Column(db.Float, default=0)
    latitude_ref = db.Column(db.String(3), default="")
    longitude = db.Column(db.Float, default=0)
    longitude_ref = db.Column(db.String(3), default="")
    altitude = db.Column(db.Float, default=0)
    altitude_ref = db.Column(db.String(3), default="")
    
    position = db.Column(db.String(30), default="")
    
    def __repr__(self):
        return '<标题: %r; 作者: %r>' % (self.title, self.author)