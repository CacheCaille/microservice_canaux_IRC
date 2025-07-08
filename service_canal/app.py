from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json 
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

class Canal(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    topic = db.Column(db.String(255), nullable=False)
    editable = db.Column(db.Boolean, default=True, nullable=False)
    private = db.Column(db.Boolean, default=False, nullable=False)
    
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)


class Role(db.Model):

    fk_user_name = db.Column(db.String(100),nullable=False, primary_key=True)
    fk_canal_name = db.Column(db.String(255), nullable=False, primary_key=True)
    role = db.Column(db.String(2), default="INVITE", nullable=False)
    banned_reason = db.Column(db.String(255), nullable=True)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
