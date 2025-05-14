from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))  # Many notes → one tag

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    notes = db.relationship('Note')
    Suggestions = db.relationship('Suggestions', backref='user_obj')  # One user, many suggestions

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(150), default="General")
    notes = db.relationship('Note', backref='tag_obj')  # One tag, many notes

class Suggestions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suggestion = db.Column(db.String(1500))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))