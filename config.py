import os


class Config(object):
    SECRET_KEY = 'HeippiPrueba'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Onemen2021@localhost/heippi"
    SECURITY_PASSWORD_SALT = "ConfirmationEmail"

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = "pruebasdesarrolloivan@gmail.com"
    MAIL_PASSWORD = "Onemen2020"

    # mail accounts
    MAIL_DEFAULT_SENDER = 'pruebasdesarrolloivan@gmail.com'
