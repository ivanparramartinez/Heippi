import os


class Config(object):
    SECRET_KEY = 'HeippiPrueba'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "postgres://hariktpwixnuwa:41f3f4dc5cc3051571b1acbf9501eb4a763aa93f97b61646e4e96f2069ebec67@ec2-3-230-106-126.compute-1.amazonaws.com:5432/d868akntnd7q88"
    SECURITY_PASSWORD_SALT = "ConfirmationEmail"

    # mail settings
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # gmail authentication
    MAIL_USERNAME = '300e0855b7add0'
    MAIL_PASSWORD = 'cd4dd85b6b8b9f'

    # mail accounts
    MAIL_DEFAULT_SENDER = 'hospitalheippi@mail.com'
    MAIL_FROM_NAME = 'Hospital Heippi'