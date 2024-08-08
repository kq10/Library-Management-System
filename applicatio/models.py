from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)  # Added for unique email address
    password_hash = db.Column(db.String(255), nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)  # Required field for Flask-Security
    active = db.Column(db.Boolean, default=True)  # Active status field
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    role = db.relationship('Role', back_populates='users')

    def __repr__(self):
        return f'<User {self.username}>'

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(255))
    users = db.relationship('User', back_populates='role')

    def __repr__(self):
        return f'<Role {self.name}>'


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Ebook(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    section = db.relationship('Section', backref=db.backref('ebooks', lazy=True))

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ebook_id = db.Column(db.Integer, db.ForeignKey('ebook.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'requested', 'granted', 'returned', 'revoked'
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    grant_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    feedback = db.Column(db.Text)

    user = db.relationship('User', backref=db.backref('requests', lazy=True))
    ebook = db.relationship('Ebook', backref=db.backref('requests', lazy=True))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ebook_id = db.Column(db.Integer, db.ForeignKey('ebook.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Rating scale (e.g., 1-5)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))
    ebook = db.relationship('Ebook', backref=db.backref('feedbacks', lazy=True))

class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_users = db.Column(db.Integer, nullable=False)
    active_users = db.Column(db.Integer, nullable=False)
    grant_requests = db.Column(db.Integer, nullable=False)
    ebooks_issued = db.Column(db.Integer, nullable=False)
    ebooks_revoked = db.Column(db.Integer, nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
