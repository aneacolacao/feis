from flask import Flask, redirect, url_for, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
# import cPickle as pickle
import json
import jsonpickle

app = Flask(__name__)

app.config.update(
  SECRET_KEY = 'iijkllioi9897sdasdjhas',
  DEBUG = True,
  SQLALCHEMY_DATABASE_URI = 'sqlite:///tmp/users_first.db', #in memory db. or use sqlite:////absolute/path/to/creeper.db,
  SQLALCHEMY_TRACK_MODIFICATIONS = True
  )
db = SQLAlchemy(app)

class Users(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  facebook_id = db.Column(db.Integer, nullable=False)
  name = db.Column(db.String(50))

  def __init__(self,facebook_id, name):
    self.facebook_id = facebook_id
    self.name = name
    # return '<User %r>' % self.name

# def save_object(obj, filename):
#     with open(filename, 'wb') as output:
#       pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

@app.route('/')
def landing():
  print ('quiero entrar al index')
  usuario = session.get('user')
  print (usuario)
  if usuario:
    print('si hay usuario')
    thawed = jsonpickle.decode(usuario)
  else:
    print('no hay usuario')
    thawed = usuario
    
  
  print(thawed) 
  return render_template('index.html', user=thawed)

# @app.route('/post')
# def post():
#   return render_template('post.html', user = session.get('user', None))


@app.route('/channel')
def channel():
  return render_template('channel.html')

@app.route('/_get_facebook_login')
def get_facebook_login():
  facebook_id = request.args.get('facebook_id', False, type=int)
  print ('aqui viene el facebook_id')
  print (facebook_id)
  name = request.args.get('name', '', type=str)
  print ('aqui viene el name')
  print (name)
  if facebook_id:
    print('si facebook_id')
    user = Users.query.filter_by(facebook_id=facebook_id).first()
    print ('aqui viene el user')
    print (user)
    # save_object(user, 'users_data .pk1')
    frozen = jsonpickle.encode(user)
    print ('soy frozen')
    print(frozen)
    thawed = jsonpickle.decode(frozen)
    print ('soy thawed')
    print(thawed)
    if not user:
      print('si no user')
      print ('aqui viene un nuevo user')
      user = Users(facebook_id,name)
      print (facebook_id)
      db.session.add(user)
      db.session.commit()
      print('creamos user')
    session['user'] = frozen
    
    # with open('users_data.pk1', 'rb') as input:
    #   user1 = pickle.load(input)
    #   print('soy pickle')
    #   print(user1.name)
    #   print(user1.facebook_id)

    print (user.name)
    print (user.facebook_id)
    print('si existe user')
    return frozen
  print('no hay user')
  return jsonify(result=1)

@app.route('/post', methods=['POST'])
def post_post():
  data = request.get_json()
  print ('aqui viene la data')
  print (data)
  session['mensaje'] = data
  return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route('/post', methods=['GET'])
def post_get():
  user_msj = session['mensaje']
  print('aqui viene el mensaje del usuario')
  print(user_msj)
  return render_template('post.html', mensaje=user_msj)
