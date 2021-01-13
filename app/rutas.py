from app import app
from flask import jsonify, request, render_template, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Users
from extensions import db
import uuid
import jwt
import datetime


@app.route('/')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = Users(public_id=str(uuid.uuid4()), personal_id=data['personal_id'], password=hashed_password,
                     email=data['email'], phone=data['phone'], kind=data['kind'], confirmed=data['confirmed'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuario Registrado'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('No se pudo verificar', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = Users.query.filter_by(personal_id=data['personal_id']).first()
    if check_password_hash(user.password, data['password']):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'])
        token_decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        return jsonify({'token': token_decoded['public_id']})

    return make_response('No se pudo verificar', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
