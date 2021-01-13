from flask import Flask
from config import Config
from extensions import db, migrate

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)

def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)

    return app

app = create_app(Config)

from app import rutas, models

if __name__ == '__main__':
    app.run()