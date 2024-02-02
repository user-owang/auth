"""auth application."""

from flask import Flask, request, redirect, render_template, flash, session
from flask_session import Session
from models import db, connect_db, User
from forms import AddUserForm, LoginForm

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'jagdf1qq393456'

connect_db(app)
with app.app_context():
        db.create_all()

@app.route('/')
def home_page():
  return render_template('home.html')

@app.route('/register', methods=['POST', 'GET'])
def registration():
  form = AddUserForm()

  if form.validate_on_submit():
    data = {k: v for k, v in form.data.items() if k != "csrf_token"}
    new_user = User.register(data['username'], data['password'], data['email'], data['first_name'], data['last_name'])
    if User.query.filter_by(username=data['username']).first():
       flash('Username already exists.')
       return redirect('/register')
    db.session.add(new_user)
    db.session.commit()
    flash("Account successfully created")
    return redirect('/secret')
  
  return render_template('registration.html', form = form)

@app.route('/login', methods=['POST', 'GET'])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    username = form.username.data
    if User.query.filter_by(username=username).first():
      flash('Username not found')
      return redirect('/login')
    password = form.password.data
    if User.authenticate(username, password):
      session['username'] = username
      return redirect('/secret')
  flash('Incorrect login information!')
  return redirect('/login')

@app.route('/secret')
def secret():
  if 'username' not in session:
    flash('Please login to continue.')
    return redirect('/login')
  return render_template('secret.html')