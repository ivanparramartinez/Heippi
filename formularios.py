from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    personal_id = StringField('Identificación', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    personal_id = StringField('Identificación', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    phone = StringField('Teléfono', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password2 = PasswordField('Repetir Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')
