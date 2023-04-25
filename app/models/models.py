from datetime import datetime
from app.database import db


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    original_name = db.Column(db.String(100), nullable=False)
    temporal_name = db.Column(db.String(), nullable=True)
    new_format = db.Column(db.String(), nullable=True)
    compressed_name = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
