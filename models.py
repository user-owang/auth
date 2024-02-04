"""models for auth"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)
bcrypt = Bcrypt()

class User(db.Model):
  __tablename__ = 'users'

  username = db.Column(db.String(20), nullable=False, unique=True, primary_key=True)
  password = db.Column(db.String, nullable=False)
  email = db.Column(db.String(50), nullable=False, unique=True)
  first_name = db.Column(db.String(30), nullable=False)
  last_name = db.Column(db.String(30), nullable=False)
  feedback = db.relationship('Feedback', cascade='all,delete-orphan', backref='author')

  @classmethod
  def register(cls, username, pwd, email, first_name, last_name):
    """register user w/hashed password & return user"""
    hashed = bcrypt.generate_password_hash(pwd)
    hashed_utf8 = hashed.decode('utf8')
    return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
  
  @classmethod
  def authenticate(cls, username, pwd):
    """Validate that user exists and password is correct and return user if valid. Else returns false"""
    u = User.query.filter_by(username=username).first()
    if u and bcrypt.check_password_hash(u.password, pwd):
      return u
    else:
      return False
    
class Feedback(db.Model):
  __tablename__ = 'posts'

  id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String, nullable=False)
  content = db.Column(db.String, nullable=False)
  author_id = db.Column(db.String, db.ForeignKey('users.username', ondelete='CASCADE'), nullable=False)
  