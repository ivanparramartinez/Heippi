from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


@login_manager.user_loader
def user_loader(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if user:
        return user
    return None


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(200))
    personal_id = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    kind = db.Column(db.String(20))
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean)
    last_logged_in = db.Column(db.DateTime)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __init__(self, public_id, personal_id, password, email, phone, kind, confirmed):
        self.public_id = public_id
        self.personal_id = personal_id
        self.password = password
        self.email = email
        self.phone = phone
        self.kind = kind
        self.registered_on = datetime.datetime.now()
        self.confirmed = confirmed

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<email {}'.format(self.email)


class HospitalUsers(db.Model, UserMixin):
    __tablename__ = 'hospitalusers'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(200))
    personal_id = db.Column(db.String(15), unique=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(300))
    medical_services = db.Column(db.String(200))
    is_doctor = db.Column(db.Boolean)
    last_logged_in = db.Column(db.DateTime)

    def __init__(self, public_id, personal_id, name, address, medical_services, last_logged_in, is_doctor):
        self.public_id = public_id
        self.personal_id = personal_id
        self.name = name
        self.address = address
        self.medical_services = medical_services
        self.last_logged_in = last_logged_in
        self.is_doctor = is_doctor


class PacientUsers(db.Model, UserMixin):
    __tablename__ = 'pacientusers'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(200))
    personal_id = db.Column(db.String(15), unique=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(300))
    dob = db.Column(db.DateTime)
    last_logged_in = db.Column(db.DateTime)

    def __init__(self, public_id, personal_id, name, address, dob, last_logged_in):
        self.public_id = public_id
        self.personal_id = personal_id
        self.name = name
        self.address = address
        self.dob = dob
        self.last_logged_in = last_logged_in


class Registros(db.Model):
    __tablename__ = 'registros'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(200))
    personal_id = db.Column(db.String(15), unique=True)
    med_obs = db.Column(db.String(200))
    spec = db.Column(db.String(50))
    estado_salud = db.Column(db.String(20))
    kind = db.Column(db.String(20))

    def __init__(self, public_id, personal_id, password, email, phone, kind, confirmed):
        self.public_id = public_id
        self.personal_id = personal_id
        self.password = password
        self.email = email
        self.phone = phone
        self.kind = kind
        self.registered_on = datetime.datetime.now()
        self.confirmed = confirmed