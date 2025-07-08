from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    db.init_app(app)
    with app.app_context():
        db.create_all()
    from controlleurs.canal_controlleur import canal_bp
    app.register_blueprint(canal_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)