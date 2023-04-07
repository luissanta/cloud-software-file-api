from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime
from app.database import db


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    original_name = db.Column(db.String(50), nullable=False)
    original_data = db.Column(db.String(50), nullable=False)
    compressed_name = db.Column(db.String(50), nullable=True)
    compressed_data = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class FileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = File
        include_relationships = True
        include_fk = True
        load_instance = True

    id = fields.Integer()
    original_name = fields.String()
    original_data = fields.String()
    compressed_name = fields.String()
    compressed_data = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
