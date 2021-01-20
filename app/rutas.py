from app import app, db
from flask import jsonify, request, render_template, flash, redirect, url_for, abort
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Users, HospitalUsers, PacientUsers, Registros, MedicalUsers
import uuid
import datetime
from app.tokens import generate_confirmation_token, confirm_token
from flask_login import login_required, login_user, logout_user, current_user
from app.email import send_email
from formularios import LoginForm, RegistrationForm, HospitalForm, PacientForm, ChangePasswordForm, MedicalForm, \
    ResetPasswordForm


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = Users.query.filter_by(personal_id=current_user.personal_id).first()
    if user.kind == 'Médico':
        hospitaluser = HospitalUsers.query.filter_by(personal_id=current_user.personal_id).first()
        if not current_user.passchn and hospitaluser.is_doctor:
            flash('Debes actualizar la contraseña para poder continuar')
            return redirect(url_for('changepassword'))
    return render_template('index.html', title='Inicio', current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        exists = bool(Users.query.filter_by(personal_id=form.personal_id.data).first())
        if exists:
            flash("El usuario ya está registrado")
            return redirect(url_for('login'))
        user = Users(public_id=str(uuid.uuid4()), personal_id=form.personal_id.data,
                     password=generate_password_hash(form.password.data), name=None, email=form.email.data,
                     phone=form.phone.data,
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
    user = Users.query.filter_by(personal_id=form.personal_id.data).first()
    if form.validate_on_submit():
        if user is None or not user.check_password(form.password.data):
            flash('Identificación o contraseña equivocados.')
            return redirect(url_for('login'))
        if not user.confirmed:
            flash('Por favor confirmar tu cuenta antes de iniciar sesión.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        if user.last_logged_in is None and user.kind == 'Hospital':
            flash('Es la primera vez que inicias sesión')
            user.last_logged_in = datetime.datetime.utcnow()
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('updatefirsthospital'))
        if user.last_logged_in is None and user.kind == 'Paciente':
            flash('Es la primera vez que inicias sesión')
            user.last_logged_in = datetime.datetime.utcnow()
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('updatefirstpacient'))
        if user.last_logged_in is None and user.kind == 'Médico':
            flash('Es la primera vez que inicias sesión')
            return redirect(url_for('changepassword'))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/updatefirsthospital', methods=['GET', 'POST'])
@login_required
def updatefirsthospital():
    if not current_user.kind == 'Hospital':
        return redirect(url_for('index'))
    user = Users.query.filter_by(personal_id=current_user.personal_id).first()
    form = HospitalForm()
    if form.validate_on_submit():
        hospitaluser = HospitalUsers(public_id=current_user.public_id, personal_id=current_user.personal_id,
                                     name=form.name.data, address=form.address.data,
                                     medical_services=form.medical_services.data, is_doctor=False, specialty=None,
                                     creator=None)
        user.name = form.name.data
        db.session.add(user)
        db.session.add(hospitaluser)
        db.session.commit()
        flash('Se ha actualizado la información')
        return redirect(url_for('index'))
    return render_template('hospital.html', title='Actualización de Datos', form=form)


@app.route('/createdoctor', methods=['GET', 'POST'])
@login_required
def createdoctor():
    if not current_user.kind == 'Hospital':
        return redirect(url_for('index'))
    form = MedicalForm()
    if form.validate_on_submit():
        hospitaluser = HospitalUsers(public_id=str(uuid.uuid4()), personal_id=form.personal_id.data,
                                     name=form.name.data, address=form.address.data,
                                     medical_services='Médico', is_doctor=True, specialty=form.specialty.data,
                                     creator=current_user.personal_id)
        user = Users(public_id=str(uuid.uuid4()), personal_id=form.personal_id.data,
                     password=generate_password_hash(form.password.data), name=form.name.data, email=form.email.data,
                     phone=form.phone.data,
                     kind='Médico', confirmed=False)
        db.session.add(hospitaluser)
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token(form.personal_id.data)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('activateuser.html', confirm_url=confirm_url)
        subject = "Confirmación de cuenta. Hospital Heippi."
        send_email(form.email.data, subject, html)
        flash('Se ha enviado un correo con el link para confirmar su cuenta.')
        flash('Se ha creado el Médico', form.name.data)
        return redirect(url_for('index'))
    return render_template('registerdoc.html', title='Creación de Médicos', form=form)


@app.route('/updatefirstpacient', methods=['GET', 'POST'])
@login_required
def updatefirstpacient():
    if not current_user.kind == 'Paciente':
        return redirect(url_for('index'))
    user = Users.query.filter_by(personal_id=current_user.personal_id).first()
    if current_user.is_authenticated and current_user.kind == 'Paciente':
        form1 = PacientForm()
        if form1.validate_on_submit():
            pacientuser = PacientUsers(public_id=current_user.public_id, personal_id=current_user.personal_id,
                                       name=form1.name.data, address=form1.address.data, dob=request.form.get('dob'),
                                       last_logged_in=current_user.last_logged_in)
            try:
                user.name = form1.name.data
                db.session.add(user)
                db.session.add(pacientuser)
                db.session.commit()
                flash('Se ha actualizado la información')
                return redirect(url_for('index'))
            except:
                flash('no actualiza')
        return render_template('pacient.html', title='Actualización de Datos', form=form1)
    else:
        return redirect(url_for('login'))


@app.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    user = Users.query.filter_by(personal_id=current_user.personal_id).first()
    hospitaluser = HospitalUsers.query.filter_by(personal_id=current_user.personal_id).first()
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if user:
            if user.check_password(form.password.data):
                flash('La contraseña no puede ser igual a la anterior')
                return redirect(url_for('changepassword'))
            else:
                if (user.last_logged_in is None) and hospitaluser.is_doctor:
                    user.last_logged_in = datetime.datetime.utcnow()
                    user.password = generate_password_hash(form.password.data)
                    user.passchn = True
                    db.session.add(user)
                    db.session.commit()
                    flash('Contraseña Actualizada')
                    return redirect(url_for('index'))
        else:
            flash('Contraseña no Actualizada')
            return redirect(url_for('changepassword'))
    return render_template('changepassword.html', form=form)


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        personal_id = confirm_token(token)
        user = Users.query.filter_by(personal_id=personal_id).first_or_404()
        if user.confirmed:
            flash('Esta cuenta ya ha sido confirmada, por favor inicie sesión.')
        else:
            user.confirmed = True
            db.session.add(user)
            db.session.commit()
            flash('¡Has confirmado tu cuenta! ¡Gracias!')
    except:
        flash('El link de confirmación es erróneo o ha expirado')
        abort(401)
    return redirect(url_for('login'))


@app.route('/resetpassword', methods=['GET', 'POST'])
def resetpassword():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        token = generate_confirmation_token(form.personal_id.data)
        user = Users.query.filter_by(personal_id=form.personal_id.data).first_or_404()
        recover_url = url_for('recover_pass', token=token, _external=True)
        html = render_template('forgotpass.html', recover_url=recover_url)
        subject = "Recuperación de Contraseña. Hospital Heippi."
        send_email(user.email, subject, html)
        flash('Se ha enviado un correo con el link para la recuperación de su contraseña.')
    return render_template('resetpassword.html', title='Recuperación de Contraseña', form=form)


@app.route('/recover_pass/<token>', methods=['GET','POST'])
def recover_pass(token):
    exists = bool(Users.query.filter_by(recover_token=token).first())
    if exists:
        flash('Este link de recuperación ya ha sido utilizado')
        return redirect(url_for('login'))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        personal_id = confirm_token(token)
        user = Users.query.filter_by(personal_id=personal_id).first_or_404()
        if not user.recover_token == token:
            if user.check_password(form.password.data):
                flash('La contraseña no puede ser igual a la anterior')
                return redirect(url_for('recover_pass'))
            else:
                user.password = generate_password_hash(form.password.data)
                user.recover_token = token
                db.session.add(user)
                db.session.commit()
                flash('Contraseña Actualizada')
                return redirect(url_for('index'))
        else:
            flash('El link de recuperación ya ha sido utilizado')
            return redirect(url_for('index'))
    return render_template('recover_pass.html', form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return render_template('logout.html', title='Home')
    else:
        return render_template('notlogged.html', title='Home')


@app.route('/consultar_registros', methods=['GET','POST'])
@login_required
def consultar_registros():
    pass
