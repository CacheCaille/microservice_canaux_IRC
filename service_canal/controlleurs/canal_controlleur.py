from flasgger import swag_from
from flask import Blueprint, jsonify, request
from repositories import canal_repository
from repositories import role_repository
from app import db
from config import Config
import jwt
import json
from flasgger import swag_from

canal_bp = Blueprint("main", __name__)

@canal_bp.route("/channel", methods=["GET"])
@swag_from({
    'tags': ['Canal'],
    'summary': 'Récupérer tous les canaux',
    'responses': {
        200: {
            'description': 'Liste de tous les canaux',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'reponse': {'type': 'array', 'items': {'type': 'object'}}
                }
            }
        }
    }
})
def get_canals():
    auth = request.headers.get("Authorization", "")
    passed = check_jwt(auth)
    if passed is None:
        return jsonify({'status': "KO", 'reponse': "Token invalide"})
    try:
        content = canal_repository.get_canals()
        return jsonify({'status': "OK", 'reponse': str(content)})
    except Exception as e:
        return jsonify({'status': "KO", 'reponse': str(e)})

@canal_bp.route("/channel/<name>/users", methods=["GET"])
@swag_from({
    'tags': ['Canal'],
    'summary': "Récupère les utilisateurs d'un canal",
    'parameters': [
        {'name': 'name', 'in': 'path', 'type': 'string', 'required': True, 'description': 'Nom du canal'}
    ],
    'responses': {
        200: {
            'description': 'Liste des utilisateurs du canal',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'reponse': {'type': 'array', 'items': {'type': 'object'}}
                }
            }
        }
    }
})
def get_canal_users(name):
    auth = request.headers.get("Authorization", "")
    passed = check_jwt(auth)
    if passed is None:
        return jsonify({'status': "KO", 'reponse': "Token invalide"})
    try:
        users = canal_repository.get_users_by_channel(name)
        return jsonify({'status': "OK", 'reponse': users})
    except Exception as e:
        return jsonify({'status': "KO", 'reponse': str(e)})

@canal_bp.route("/channel/<name>/config", methods=["GET"])
@swag_from({
    'tags': ['Canal'],
    'summary': "Récupère la configuration d'un canal",
    'parameters': [
        {'name': 'name', 'in': 'path', 'type': 'string', 'required': True, 'description': 'Nom du canal'}
    ],
    'responses': {
        200: {
            'description': 'Configuration du canal',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'reponse': {'type': 'object'}
                }
            }
        }
    }
})
def get_canal_config(name):
    auth = request.headers.get("Authorization", "")
    passed = check_jwt(auth)
    if passed is None:
        return jsonify({'status': "KO", 'reponse': "Token invalide"})
    try:
        config = canal_repository.get_channel_config(name)
        return jsonify({'status': "OK", 'reponse': config})
    except Exception as e:
        return jsonify({'status': "KO", 'reponse': str(e)})

@canal_bp.route("/channel/topActivity", methods=["GET"])
@swag_from({
    'tags': ['Canal'],
    'summary': "Récupérer le canal ayant le plus d'activité (le plus d'utilisateurs)",
    'responses': {
        200: {
            'description': "Le canal qui a le plus d'activité",
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'reponse': {'type': 'array', 'items': {'type': 'object'}}
                }
            }
        }
    }
})
def get_canal_top_activity(channel_name):
    auth = request.headers.get("Authorization", "")
    passed = check_jwt(auth)
    if passed is None:
        return jsonify({'status': "KO", 'reponse': "Token invalide"})
    raise Exception("Not implemented yet")

@canal_bp.route("/channel", methods=["POST"])
@swag_from({
    'tags': ['Canal'],
    'summary': "Crée un canal",
    'parameters': [
        {'name': 'Authorization', 'in': 'header', 'type': 'string', 'required': True},
        {'name': 'body', 'in': 'body', 'schema': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'example': 'général',
                        'description': 'Nom du canal à créer'
                    },
                    'private': {
                        'type': 'boolean',
                        'example': False,
                        'description': 'Indique si le canal est privé (true) ou public (false)'
                    }
                },
                'required': ['name', 'private']
            }}
    ],
    'responses': {
        200: {
            'description': 'Le canal créé',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'reponse': {'type': 'object'}
                }
            }
        }
    }
})
def create_canal():
    auth = request.headers.get("Authorization", "")
    passed = check_jwt(auth)
    if passed is None:
        return jsonify({'status': "KO", 'reponse': "Token invalide"})
    try:
        data = request.get_json()
        canal = canal_repository.create_canal(data.get("name"),data.get("private"))
        return jsonify({'status': "OK", 'reponse': str(canal)})
    except Exception as e:
        return jsonify({'status': "KO", 'reponse': str(e)})

@canal_bp.route("/channel/<name>/topic", methods=["POST"])
@swag_from({
    'tags': ['Canal'],
    'summary': "Met à jour le sujet d'un canal",
    'parameters': [
        {'name': 'name', 'in': 'path', 'type': 'string', 'required': True, 'description': 'Nom du canal'},
        {'name': 'body', 'in': 'body', 'schema': {
            'type': 'object',
            'properties': {
                'topic': {'type': 'string', 'example': 'Sujet du canal'}

            },
            'required': ['topic']
        }}
    ],
    'responses': {
        200: {
            'description': 'Le canal modifié',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'reponse': {'type': 'object'}
                }
            }
        }
    }
})
def update_canal_topic(name):
    auth = request.headers.get("Authorization", "")
    passed = check_jwt(auth)
    if passed is None:
        return jsonify({'status': "KO", 'reponse': "Token invalide"})
    try:
        body = request.get_json()
        topic = body.get("topic")
        content = canal_repository.update_canal_topic(name, topic)
        return jsonify({'status': "OK", 'reponse': "Le topic a ete mis a jour"})
    except Exception as e:
        return jsonify({'status': "KO", 'reponse': str(e)})

@canal_bp.route("/channel/<name>/mode", methods=["POST"])
@swag_from({
    'tags': ['Canal'],
    'summary': "Met à jour le mode d'un canal",
    'parameters': [
        {'name': 'name', 'in': 'path', 'type': 'string', 'required': True, 'description': 'Nom du canal'},
        {'name': 'body', 'in': 'body', 'schema': {
            'type': 'object',
            'properties': {
                'mode': {'type': 'string', 'example': 'r+ (rw: lecture/écriture, + public / - privé)'}
            },
            'required': ['mode']
        }}
    ],
    'responses': {
        200: {
            'description': 'Le canal modifié',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'reponse': {'type': 'object'}
                }
            }
        }
    }
})
def update_canal_mode(name):
    auth = request.headers.get("Authorization", "")
    passed = check_jwt(auth)
    if passed is None:
        return jsonify({'status': "KO", 'reponse': "Token invalide"})
    try:
        body = request.get_json()
        editable = None
        private = None
        if body.get("mode")[0] == 'r':
            editable = False
        elif body.get("mode")[0] == 'w':
            editable = True

        if body.get("mode")[1] == '+':
            private = False
        elif body.get("mode")[1] == '-':
            private = True

        if editable is None or private is None:
            raise Exception("Le mode ", body.get("mode"), " n'est pas un mode valide")

        canal_repository.update_canal_mode(name, editable, private)
        return jsonify({'status': "OK", 'reponse': "Le mode a ete mis a jour"})
    except Exception as e:
        return jsonify({'status': "KO", 'reponse': str(e)})

@canal_bp.route("/channel/<name>/invite", methods=["POST"])
@swag_from({
    'tags': ['Canal'],
    'summary': 'Invite un utilisateur dans un canal (MODERATOR ou OWNER seulement)',
    'parameters': [
        {'name': 'name', 'in': 'path', 'type': 'string', 'required': True, 'description': 'Nom du canal'},
        {'name': 'Authorization', 'in': 'header', 'type': 'string', 'required': True},
        {'name': 'body', 'in': 'body', 'schema': {
            'type': 'object',
            'properties': {
                'pseudo': {'type': 'string'}
            },
            'required': ['pseudo']
        }}
    ],
    'responses': {
        200: {
            'description': "L'utilisateur invité",
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'reponse': {'type': 'object'}
                }
            }
        }
    }
})
def invite_user_to_canal(channel_name):
    auth = request.headers.get("Authorization", "")
    passed = check_jwt(auth)
    if passed is None:
        return jsonify({'status': "KO", 'reponse': "Token invalide"})
    role = role_repository.get_user_roles(channel_name, passed)
    if role.role == "OWNER" or role.role == "MODERATOR":
        # Logic to invite user to channel
        data = request.get_json()
        data.get("pseudo")
        role_repository.insert_user(data.get("pseudo"), channel_name, role="INVITE")
        return jsonify({'status': "OK", 'reponse': f"User invited to channel {channel_name}"})
    else :
        return jsonify({'status': "KO", 'reponse': "You are not authorized to invite users to this channel"})

@canal_bp.route("/channel/<name>/ban", methods=["POST"])
@swag_from({
    'tags': ['Canal'],
    'summary': 'Bannit un utilisateur du canal (OWNER seulement)',
    'parameters': [
        {'name': 'name', 'in': 'path', 'type': 'string', 'required': True, 'description': 'Nom du canal'},
        {'name': 'Authorization', 'in': 'header', 'type': 'string', 'required': True},
        {'name': 'body', 'in': 'body', 'schema': {
            'type': 'object',
            'properties': {
                'pseudo': {'type': 'string'},
                'banned_reason': {'type': 'string'}
            },
            'required': ['pseudo']
        }}
    ],
    'responses': {
        200: {
            'description': "L'utilisateur banni",
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'reponse': {'type': 'object'}
                }
            }
        }
    }
})
def ban_user_from_channel(channel_name):
    auth = request.headers.get("Authorization", "")
    passed = check_jwt(auth)
    if passed is None:
        return jsonify({'status': "KO", 'reponse': "Token invalide"})
    role = role_repository.get_user_roles(channel_name, passed)
    if role == "OWNER":
        # Logic to ban user from channel
        data = request.get_json()
        data.get("pseudo")
        role = role_repository.get_user_roles(channel_name, data.get("pseudo"))
        role.banned_reason = data.get("banned_reason", "No reason provided")
        role.role = "BANNED"
        db.session.commit() # ^^ Il faudrait pas avoir ça là mais on a pas le temp de ce coordonnée pour faire un services
        return jsonify({'status': "OK", 'reponse': f"User banned from channel {channel_name}"})
    else :
        return jsonify({'status': "KO", 'reponse': "You are not authorized to ban users from this channel"})

@canal_bp.route("/channel/<name>", methods=["PATCH"])
@swag_from({
    'tags': ['Canal'],
    'summary': 'Modifie le canal (sujet + mode)',
    'parameters': [
        {'name': 'name', 'in': 'path', 'type': 'string', 'required': True, 'description': 'Nom du canal'},
        {'name': 'body', 'in': 'body', 'schema': {
            'type': 'object',
            'properties': {
                'topic': {'type': 'string', 'example': 'Sujet du canal'},
                'mode': {'type': 'string', 'example': 'r+ (rw: lecture/écriture, + public / - privé)'}
            },
            'required': ['topic', 'mode']
        }}
    ],
    'responses': {
        200: {
            'description': "Le canal modifié",
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'reponse': {'type': 'object'}
                }
            }
        }
    }
})
def modify_canal(name):
    auth = request.headers.get("Authorization", "")
    passed = check_jwt(auth)
    if passed is None:
        return jsonify({'status': "KO", 'reponse': "Token invalide"})
    try:
        body = request.get_json()
        topic = body["topic"]

        if body.get("mode")[0] == 'r':
            editable = False
        elif body.get("mode")[0] == 'w':
            editable = True

        if body.get("mode")[1] == '+':
            private = False
        elif body.get("mode")[1] == '-':
            private = True

        if editable is None or private is None:
            raise Exception("Le mode ", body.get("mode"), " n'est pas un mode valide")

        content = canal_repository.update_canal_topic_and_mode(name, topic, editable, private)
        return jsonify({'status': "OK", 'reponse': "Canal mis a jour"})
    except Exception as e:
        return jsonify({'status': "KO", 'reponse': str(e)})

@canal_bp.route("/channel/<canal_nom>", methods=["DELETE"])
@swag_from({
    'tags': ['Canal'],
    'summary': 'Supprime un canal',
    'parameters': [
        {'name': 'name', 'in': 'path', 'type': 'string', 'required': True, 'description': 'Nom du canal'},
        {'name': 'Authorization', 'in': 'header', 'type': 'string', 'required': True}
    ],
    'responses': {
        200: {
            'description': "Le canal supprimé",
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'reponse': {'type': 'object'}
                }
            }
        }
    }
})
def delete_canal(canal_nom):
    auth = request.headers.get("Authorization", "")
    passed = check_jwt(auth)
    if passed is None:
        return jsonify({'status': "KO", 'reponse': "Token invalide"})
    try:
        canal = canal_repository.del_canal(canal_nom)
        return jsonify({'status': "OK", 'reponse': str(canal)})
    except Exception as e:
        return jsonify({'status': "KO", 'reponse': str(e)})



def check_jwt(auth):
    if not auth.startswith("Bearer "):
        return None
    token = auth[7:]
    try:
        decoded = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        return decoded["pseudo"]
    except:
        return None
    return None
