from flask import Flask
from config import Config
from extensions import db, migrate
from flask_mail import Mail
from flask_login import LoginManager


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)

    return app


app = create_app(Config)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


from app import rutas, models


app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

if __name__ == '__main__':
    app.run()