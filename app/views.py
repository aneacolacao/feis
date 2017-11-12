# from flask import Flask, redirect, url_for, render_template, request, jsonify, session
# from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from app import app

app = Flask(__name__)
app.config.update(
  SECRET_KEY = 'sdasdkjafld98989',
  DEBUG = True,
  SQLALCHEMY_DATABASE_URI = 'sqlite://', #in memory db. or use sqlite:////absolute/path/to/creeper.db,
  # SQLALCHEMY_TRACK_MODIFICATIONS = True
  )
# db = SQLAlchemy(app)

# class Users(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   facebook_id = db.Column(db.Integer)
#   name = db.Column(db.String(50))

#   def __init__(self,facebook_id, name):
#     self.facebook_id = facebook_id
#     self.name = name

@app.route('/')
def landing():
  print ('quiero entrar al index')	
  return render_template('index.html', user=None)

@app.route('/channel')
def channel():
  return render_template('channel.html')

# @app.route('/_get_facebook_login')
# def get_facebook_login():
#   facebook_id = request.args.get('facebook_id', False, type=int)
#   name = request.args.get('name', '', type=str)
#   if facebook_id:
#     user = Users.query.filter_by(facebook_id=facebook_id).first()
#     if not user:
#       user = Users(facebook_id,name)
#       db.session.add(user)
#       db.session.commit()
#     session['user'] = user
#   return jsonify(result=1)

@app.route('/post')
def post():
  return render_template('post.html')