from setup import db
from datetime import datetime
from sqlalchemy import ForeignKey
from models.user import User

class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    file_name = db.Column(db.String(255), nullable=False, unique=True)
    file_path = db.Column(db.String(255),nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    udadated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)