from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, EqualTo, Email, Length


class LoginForm(FlaskForm):
    personal_id = StringField('Identificación', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar Sesión')


class RegistrationForm(FlaskForm):
    personal_id = StringField('Identificación', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    phone = StringField('Teléfono', validators=[DataRequired()])
    kind = SelectField('Tipo', choices=['Hospital', 'Paciente'])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6, max=255)])
    password2 = PasswordField('Repetir Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')


class HospitalForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    address = StringField('Dirección', validators=[DataRequired()])
    medical_services = StringField('Servicios Médicos', validators=[DataRequired()])
    submit = SubmitField('Actualizar Datos')


class MedicalForm(FlaskForm):
    personal_id = StringField('Identificación', validators=[DataRequired()])
    name = StringField('Nombre', validators=[DataRequired()])
    address = StringField('Dirección', validators=[DataRequired()])
    specialty =  SelectField('Especialidad', choices=['General', 'Cirugía', 'Medicina Interna', 'Fisiatría','Pediatría'])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    phone = StringField('Teléfono', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6, max=255)])
    password2 = PasswordField('Repetir Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Crear Médico')


class PacientForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    address = StringField('Dirección', validators=[DataRequired()])
    dob = DateField('Fecha de Nacimiento', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Actualizar Datos')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6, max=255)])
    password2 = PasswordField('Repetir Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Actualizar Contraseña')
