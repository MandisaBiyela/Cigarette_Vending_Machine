from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class CigaretteBrand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    purchases = db.relationship('Purchase', backref='brand', lazy=True)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('cigarette_brand.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
