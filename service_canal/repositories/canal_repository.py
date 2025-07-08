from app import Canal
from app import db

def get_canals():
    """
    Retrieve all channels.
    """
    return Canal.query.all()


def create_canal(nom_canal,private_canal):
	
	canal = Canal(name=nom_canal, private=private_canal, topic="")
	db.session.add(canal)
	db.session.commit()

def del_canal(nom_canal):
    Canal.query.filter(Canal.name==nom_canal).delete()
    db.session.commit()
