from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    db.init_app(app)
    from app.controlleurs.canal_controlleur import canal_bp
    app.register_blueprint(canal_bp)

    return app
