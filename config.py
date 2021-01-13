import os

class Config(object):
    SECRET_KEY = os.urandom(32)
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Onemen2021@localhost/heippi"