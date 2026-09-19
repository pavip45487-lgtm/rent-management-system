from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20))
    name = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    properties = db.relationship('Property', backref='owner', lazy=True)
    wishlist = db.relationship('Wishlist', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    purpose = db.Column(db.String(50))
    property_type = db.Column(db.String(50))
    price = db.Column(db.Float)
    deposit = db.Column(db.Float)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    balcony = db.Column(db.Integer)
    parking = db.Column(db.String(50))
    area_size = db.Column(db.String(50))
    floor = db.Column(db.String(50))
    facing = db.Column(db.String(50))
    furnished = db.Column(db.String(50))
    water = db.Column(db.String(50))
    electricity = db.Column(db.String(50))
    internet = db.Column(db.String(50))
    address = db.Column(db.String(255))
    locality = db.Column(db.String(120))
    city = db.Column(db.String(120))
    district = db.Column(db.String(120))
    state = db.Column(db.String(120))
    pincode = db.Column(db.String(20))
    google_map = db.Column(db.String(255))
    owner_name = db.Column(db.String(120))
    owner_phone = db.Column(db.String(50))
    owner_email = db.Column(db.String(120))
    available_from = db.Column(db.String(50))
    images = db.Column(db.Text)  # comma separated filenames
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    property = db.relationship('Property', backref='wishlisted')
