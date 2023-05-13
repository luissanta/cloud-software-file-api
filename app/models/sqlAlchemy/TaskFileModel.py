from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from .declarative_base import Base

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    original_name = Column(String(100), nullable=False)
    temporal_name = Column(String(), nullable=True)
    new_format = Column(String(), nullable=True)
    compressed_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    task_id = Column(String(128))
    file_name = Column(String(255))
    original_extension = Column(String(128))
    new_extension = Column(String(128))
    status = Column(String(128))
    id_user = Column(Integer)
    id_original_file = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)