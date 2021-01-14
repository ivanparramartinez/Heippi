from app import app, db
from flask import jsonify, request, render_template, make_response, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Users, HospitalUsers, PacientUsers
import uuid
import datetime
from app.tokens import generate_confirmation_token, confirm_token
from flask_login import login_required, login_user, logout_user, current_user
from app.email import send_email
from formularios import LoginForm, RegistrationForm, HospitalForm, PacientForm


@app.route('/')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        exists = bool(Users.query.filter_by(personal_id=form.personal_id.data).first())
        if exists:
            flash("El usuario ya está registrado")
            return redirect(url_for('index'))
        user = Users(public_id=str(uuid.uuid4()), personal_id=form.personal_id.data,
                     password=generate_password_hash(form.password.data), email=form.email.data, phone=form.phone.data,
                     kind=request.form.get('kind'), confirmed=False)
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token(form.personal_id.data)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('activateuser.html', confirm_url=confirm_url)
        subject = "Confirmación de cuenta. Hospital Heippi."
        send_email(form.email.data, subject, html)
        flash('Se ha enviado un correo con el link para confirmar su cuenta.')
        return redirect(url_for('login'))
    dropdown_list = ['Hospital', 'Paciente']
    return render_template('register.html', title='Register', form=form, dropdown_list=dropdown_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(personal_id=form.personal_id.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Identificación o contraseña equivocados.')
            return redirect(url_for('login'))
        if not user.confirmed:
            flash('Por favor confirmar tu cuenta antes de iniciar sesión.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        if user.last_logged_in is None:
            flash('Es la primera vez que inicias sesión')
            user.last_logged_in = datetime.datetime.utcnow()
            db.session.add(user)
            db.session.commit()
        if user.kind == 'Hospital':
            exists = bool(HospitalUsers.query.filter_by(personal_id=form.personal_id.data).first())
            if exists:
                hospitaluser = HospitalUsers.query.filter_by(personal_id=form.personal_id.data).first()
                if (hospitaluser.name is None) or (hospitaluser.address is None) or (
                        hospitaluser.medical_services is None):
                    flash('Hospital')
                    return redirect(url_for('updatefirsthospital'))
            else:
                flash('Hospital')
                return redirect(url_for('updatefirsthospital'))
        else:
            exists2 = bool(PacientUsers.query.filter_by(personal_id=form.personal_id.data).first())
            if exists2:
                pacientuser = PacientUsers.query.filter_by(personal_id=form.personal_id.data).first()
                if (pacientuser.name is None) or (pacientuser.address is None) or (
                        pacientuser.dob is None):
                    flash('Paciente')
                    return redirect(url_for('updatefirstpacient'))
            else:
                flash('Paciente')
                return redirect(url_for('updatefirstpacient'))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return render_template('logout.html', title='Home')
    else:
        return render_template('notlogged.html', title='Home')


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        personal_id = confirm_token(token)
    except:
        flash('El link de confirmación es erróneo o ha expirado')
    user = Users.query.filter_by(personal_id=personal_id).first_or_404()
    if user.confirmed:
        flash('Esta cuenta ya ha sido confirmada, por favor inicie sesión.')
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash('¡Has confirmado tu cuenta! ¡Gracias!')
    return redirect(url_for('login'))


@app.route('/updatefirsthospital', methods=['GET', 'POST'])
def updatefirsthospital():
    if current_user.is_authenticated and current_user.kind == 'Hospital':
        form = HospitalForm()
        if form.validate_on_submit():
            hospitaluser = HospitalUsers(public_id=current_user.public_id, personal_id=current_user.personal_id,
                                         name=form.name.data, address=form.address.data,
                                         medical_services=form.medical_services.data, is_doctor=form.is_doctor.data,
                                         last_logged_in=current_user.last_logged_in)
            db.session.add(hospitaluser)
            db.session.commit()
            flash('Se ha actualizado la información')
            return redirect(url_for('index'))
        return render_template('hospital.html', title='Actualización de Datos', form=form)
    else:
        return redirect(url_for('login'))


@app.route('/updatefirstpacient', methods=['GET', 'POST'])
def updatefirstpacient():
    if current_user.is_authenticated and current_user.kind == 'Paciente':
        form1 = PacientForm()
        if form1.validate_on_submit():
            pacientuser = PacientUsers(public_id=current_user.public_id, personal_id=current_user.personal_id,
                                       name=form1.name.data, address=form1.address.data, dob=request.form.get('dob'),
                                       last_logged_in=current_user.last_logged_in)
            try:
                db.session.add(pacientuser)
                db.session.commit()
                flash('Se ha actualizado la información')
                return redirect(url_for('index'))
            except:
                flash('no actualiza')
        return render_template('pacient.html', title='Actualización de Datos', form=form1)
    else:
        return redirect(url_for('login'))
