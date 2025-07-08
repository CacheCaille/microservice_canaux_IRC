from app import Canal, Role
from app import db

def get_canals():
    """
    Retrieve all channels.
    """
    return Canal.query.filter(Canal.private=='false').all()

def update_canal_topic(name, topic):
    return Canal.query.filter_by(name=name).update({'topic': topic})

def update_canal_mode(name, editable, private):
    return Canal.query.filter_by(name=name).update({'editable': editable, 'private': private})

def update_canal_topic_and_mode(name, topic, editable, private):
    return Canal.query.filter_by(name=name).update({'topic': topic, 'editable': editable, 'private': private})

def get_users_by_channel(channel_name):
    """
    Renvoie la liste des utilisateurs d'un canal.
    """
    canal = Canal.query.filter_by(nom=channel_name).first()
    if not canal:
        raise Exception("Canal non trouvé.")

    roles = Role.query.filter_by(CanalName=channel_name).all()
    return [
        {"username": r.UserName, "role": r.Role}
        for r in roles if r.Role != "banned"
    ]

def get_channel_config(channel_name):
    """
    Renvoie la configuration complète d un canal (topic, mode, private, rôles).
    """
    canal = Canal.query.filter_by(nom=channel_name).first()
    if not canal:
        raise Exception("Canal non trouvé.")

    roles = Role.query.filter_by(CanalName=channel_name).all()

    return {
        "nom": canal.nom,
        "private": canal.Private,
        "topic": canal.Topic,
        "roles": [
            {
                "username": r.UserName,
                "role": r.Role,
                "ban_reason": r.BanedReason
            }
            for r in roles
        ]
    }

def create_canal(nom_canal,private_canal):
	
	canal = Canal(name=nom_canal, private=private_canal, topic="")
	db.session.add(canal)
	db.session.commit()

def del_canal(nom_canal):
    Canal.query.filter(Canal.name==nom_canal).delete()
    db.session.commit()
