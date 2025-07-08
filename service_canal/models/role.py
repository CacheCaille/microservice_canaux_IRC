from app import db

class Role(db.Model):

    fk_user_name = db.Column(db.String(100),nullable=False, primary_key=True)
    fk_canal_name = db.Column(db.String(255), nullable=False, primary_key=True)
    role = db.Column(db.String(2), default="w+", nullable=False)
    banned_reason = db.Column(db.String(255), nullable=True)
