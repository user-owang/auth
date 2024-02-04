"""auth application."""

from flask import Flask, request, redirect, render_template, flash, session
from flask_session import Session
from models import db, connect_db, User, Feedback
from forms import AddUserForm, LoginForm, FeedbackForm

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
  if session.get('username'):
    return redirect(f'/users/{session["username"]}')

  if form.validate_on_submit():
    data = {k: v for k, v in form.data.items() if k != "csrf_token"}
    new_user = User.register(data['username'], data['password'], data['email'], data['first_name'], data['last_name'])
    if User.query.filter_by(username=data['username']).first():
       flash('Username already exists.')
       return redirect('/register')
    db.session.add(new_user)
    db.session.commit()
    session['username'] = new_user.username
    flash("Account successfully created")
    return redirect(f'/users/{session["username"]}')
  
  return render_template('registration.html', form = form)

@app.route('/login', methods=['POST', 'GET'])
def login():
  form = LoginForm()

  if session.get('username'):
    return redirect(f'/users/{session["username"]}')
  
  if form.validate_on_submit():
    username = form.username.data
    if not User.query.filter_by(username=username).first():
      flash('Username not found')
      return redirect('/login')
    password = form.password.data
    if User.authenticate(username, password):
      session['username'] = username
      return redirect(f'/users/{session["username"]}')
    flash('Incorrect login info.')
    return redirect('/login')
  return render_template('login.html', form=form)

@app.route('/users/<username>')
def secret(username):
  if 'username' not in session:
    flash('Please login to continue.')
    return redirect('/login')
  user = User.query.get_or_404(username)
  return render_template('user.html', user=user)

@app.route('/logout')
def logout():
  session.pop('username')
  return redirect('/')

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
  if session.get('username') != username:
    flash('You are not authorized to delete this user!')
    if session.get('username'):
      return redirect(f'/users/{session["username"]}')
    else:
      return redirect('/login')
  User.query.filter_by(username=username).delete()
  db.session.commit()
  session.clear()
  flash('Account successfully deleted!')
  return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
  user_page = User.query.get_or_404(username)
  if session.get('username') != username:
    flash(f'You are not logged in as {username}!')
    if session.get('username'):
      return redirect(f'/users/{session["username"]}')
    else:
      return redirect('/login')
  
  form = FeedbackForm()
  if form.validate_on_submit():
    title = form.title.data
    content = form.content.data
    post = Feedback(title=title, content=content, author_id=username)
    db.session.add(post)
    db.session.commit()
    flash('Feedback submitted!')
    return redirect(f'/users/{username}')
  return render_template('feedback.html', form=form, user=user_page)

@app.route('/feedback/<int:id>/update', methods=['GET', 'POST'])
def update_feedback(id):
  post = Feedback.query.get_or_404(id)
  if session.get('username') != post.author_id:
    flash(f'You are not authorized to edit this feedback!')
    if session.get('username'):
      return redirect(f'/users/{session["username"]}')
    else:
      return redirect('/login')
  
  form = FeedbackForm(obj=post)
  if form.validate_on_submit():
    post.title = form.title.data
    post.content = form.content.data
    
    db.session.commit()
    flash('Feedback edited!')
    return redirect(f'/users/{post.author_id}')
  return render_template('edit-feedback.html', form=form, post=post)\
  
@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
  post = Feedback.query.get_or_404
  if session.get('username') != post.author_id:
    flash('You are not authorized to delete this feedback!')
    if session.get('username'):
      return redirect(f'/users/{session["username"]}')
    else:
      return redirect('/login')
    
  Feedback.query.filter_by(id=id).delete()
  db.session.commit()
  flash('Feedback successfully deleted!')
  return redirect(f'/users/{session["username"]}')