from ..core import db
from ..helpers import JsonSerializer


class VendorSerializer(JsonSerializer):
    __json_hidden__ = ['tasks']


class Vendor(VendorSerializer, db.Model):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    price_range = db.Column(db.String(255))
    profile_image = db.Column(db.String(512))
    cover_image = db.Column(db.String(512))
    website = db.Column(db.String(512))
