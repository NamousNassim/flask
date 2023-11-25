from . import db 
from sqlalchemy import func
from flask_login import UserMixin
class Note(db.Model) : 
    id = db.Column(db.Integer , primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True) , default =func.now())
    id_user = db.Column(db.Integer , db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    email = db.Column(db.String(150) , unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(100) , unique=True)
    notes = db.relationship('Note')