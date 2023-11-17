from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from uuid import uuid4

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.String(64), primary_key=True, default=str(uuid4()))
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


    def __init__(self, username, email, password):
        self.id = str(uuid4())
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def create(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, username=None, email=None, password=None):
        if username:
            self.username = username
        if email:
            self.email = email
        if password:
            self.password = generate_password_hash(password)
        db.session.commit()
        
    def to_response(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

