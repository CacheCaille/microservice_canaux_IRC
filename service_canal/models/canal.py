from .. import db

class Canal(db.Model):
    __tablename__ = 'canal'
    
    name = db.Column(db.String(100), primary_key=True)
    topic = db.Column(db.String(255), nullable=False)
    editable = db.Column(db.Boolean, default=True, nullable=False)
    private = db.Column(db.Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f'<Canal {self.name}>'