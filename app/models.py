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
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    kind = db.Column(db.String(20))
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean)
    last_logged_in = db.Column(db.DateTime)
    passchn = db.Column(db.Boolean)
    recover_token = db.Column(db.String(200))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __init__(self, public_id, personal_id, password, name, email, phone, kind, confirmed):
        self.public_id = public_id
        self.personal_id = personal_id
        self.password = password
        self.name = name
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

    __mapper_args__ = {
        'polymorphic_on': kind,
    }


class HospitalUsers(db.Model, UserMixin):
    __tablename__ = 'hospitalusers'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(200))
    personal_id = db.Column(db.String(15), unique=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(300))
    medical_services = db.Column(db.String(200))
    is_doctor = db.Column(db.Boolean)
    dob = db.Column(db.Date)
    specialty = db.Column(db.String(200))
    creator = db.Column(db.String(200))

    def __init__(self, public_id, personal_id, name, address, medical_services, is_doctor, specialty, creator):
        self.public_id = public_id
        self.personal_id = personal_id
        self.name = name
        self.address = address
        self.medical_services = medical_services
        self.is_doctor = is_doctor
        self.specialty = specialty
        self.creator = creator


class MedicalUsers(db.Model, UserMixin):
    __tablename__ = 'medicalusers'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(200))
    personal_id = db.Column(db.String(15), unique=True)
    hosp_user_pid = db.Column(db.String(15))
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    address = db.Column(db.String(300))
    specialty = db.Column(db.String(200))
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, public_id, personal_id, hosp_user_id, name, email, phone, address, specialty):
        self.public_id = public_id
        self.personal_id = personal_id
        self.hosp_user_pid = hosp_user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.specialty = specialty
        self.registered_on = datetime.datetime.now()


class PacientUsers(db.Model, UserMixin):
    __tablename__ = 'pacientusers'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(200))
    personal_id = db.Column(db.String(15), unique=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(300))
    dob = db.Column(db.Date)

    def __init__(self, public_id, personal_id, name, address, dob, last_logged_in):
        self.public_id = public_id
        self.personal_id = personal_id
        self.name = name
        self.address = address
        self.dob = dob


class Registros(db.Model):
    __tablename__ = 'registros'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.String(15), unique=True)
    medico_id = db.Column(db.String(15))
    specialty = db.Column(db.String(50))
    med_obs = db.Column(db.String(500))
    estado_salud = db.Column(db.String(50))
    med_creator_id = db.Column(db.String(15))
    created_on = db.Column(db.DateTime, nullable=False)
    last_modifying = db.Column(db.DateTime, nullable=False)

    def __init__(self, paciente_id, medico_id, specialty, med_obs, estado_salud, med_creator_id, created_on, last_modifying):
        self.paciente_id = paciente_id
        self.medico_id = medico_id
        self.specialty = specialty
        self.med_obs = med_obs
        self.estado_salud = estado_salud
        self.med_creator_id = med_creator_id
        self.created_on = created_on
        self.last_modifying = last_modifying