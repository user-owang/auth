from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length

class AddUserForm(FlaskForm):
  """form for user registration"""
  username = StringField("Username*", validators=[InputRequired(), Length(max=20, message='Username cannot exceed 20 characters')])
  password = PasswordField('Password*', validators=[InputRequired()])
  email = StringField('Email*', validators=[InputRequired(), Email(message='Please enter a valid email address'), Length(max=50, message='Email cannot exceed 50 characters')])
  first_name = StringField('First Name*', validators=[InputRequired(), Length(max=30, message='First name cannot exceed 30 characters')])
  last_name = StringField('Last Name*', validators=[InputRequired(), Length(max=30, message='Last name cannot exceed 30 characters')])

class LoginForm(FlaskForm):
  """form for user login"""
  username = StringField('Username', validators=[InputRequired()])
  password = PasswordField('Password', validators=[InputRequired()])

class FeedbackForm(FlaskForm):
  """form to post new feedback"""
  title = StringField('Title', validators=[InputRequired(), Length(max=100, message='Title cannot exceed 100 characters')])
  content = TextAreaField('Content', validators=[InputRequired()])