from .. import db

class Roles(db.Model):
    __tablename__ = 'roles'
    
    fk_user_name = db.Column(db.String(100),nullable=False, primary_key=True)
    fk_canal_name = db.Column(db.String(255), nullable=False, primary_key=True)
    role = db.Column(db.String(2), default="w+", nullable=False)
    banned_reason = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f'<Canal {self.name}>'