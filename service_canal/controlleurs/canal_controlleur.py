from flask import Blueprint, jsonify, request
from repositories import canal_repository
from repositories import role_repository
from app import db
import jwt
import json 
from flasgger import swag_from

canal_bp = Blueprint("main", __name__)

@canal_bp.route("/channel", methods=["GET"])
@swag_from({
    'tags': ['Canaux'],
    'summary': 'Récupérer tous les canaux',
    'description': 'Retourne la liste de tous les canaux disponibles',
    'responses': {
        200: {
            'description': 'Liste des canaux récupérée avec succès',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'OK'},
                    'reponse': {'type': 'string', 'description': 'Liste des canaux sous forme de string'}
                }
            }
        },
        500: {
            'description': 'Erreur serveur',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'KO'},
                    'reponse': {'type': 'string', 'description': 'Message d\'erreur'}
                }
            }
        }
    }
})
def get_canals():
    try:
        content = canal_repository.get_canals()
        return jsonify({'status': "OK", 'reponse': str(content)})
    except Exception as e:
        return jsonify({'status': "KO", 'reponse': str(e)})

@canal_bp.route("/channel/<name>/users", methods=["GET"])
@swag_from({
    'tags': ['Canaux'],
    'summary': 'Récupérer les utilisateurs d\'un canal',
    'description': 'Retourne la liste des utilisateurs d\'un canal spécifique',
    'parameters': [
        {
            'name': 'name',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Nom du canal'
        }
    ],
    'responses': {
        200: {
            'description': 'Liste des utilisateurs récupérée avec succès',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'OK'},
                    'reponse': {'type': 'array', 'items': {'type': 'object'}}
                }
            }
        },
        500: {
            'description': 'Erreur serveur',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'KO'},
                    'reponse': {'type': 'string', 'description': 'Message d\'erreur'}
                }
            }
        }
    }
})
def get_canal_users(name):
    try:
        users = canal_repository.get_users_by_channel(name)
        return jsonify({'status': "OK", 'reponse': users})
    except Exception as e:
        return jsonify({'status': "KO", 'reponse': str(e)})

@canal_bp.route("/channel/<name>/config", methods=["GET"])
@swag_from({
    'tags': ['Canaux'],
    'summary': 'Récupérer la configuration d\'un canal',
    'description': 'Retourne la configuration d\'un canal spécifique',
    'parameters': [
        {
            'name': 'name',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Nom du canal'
        }
    ],
    'responses': {
        200: {
            'description': 'Configuration récupérée avec succès',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'OK'},
                    'reponse': {'type': 'object', 'description': 'Configuration du canal'}
                }
            }
        },
        500: {
            'description': 'Erreur serveur',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'KO'},
                    'reponse': {'type': 'string', 'description': 'Message d\'erreur'}
                }
            }
        }
    }
})
def get_canal_config(name):
    try:
        config = canal_repository.get_channel_config(name)
        return jsonify({'status': "OK", 'reponse': config})
    except Exception as e:
        return jsonify({'status': "KO", 'reponse': str(e)})

@canal_bp.route("/channel/topActivity", methods=["GET"])
@swag_from({
    'tags': ['Canaux'],
    'summary': 'Récupérer les canaux les plus actifs',
    'description': 'Retourne les canaux avec la plus grande activité (non implémenté)',
    'responses': {
        500: {
            'description': 'Fonctionnalité non implémentée',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'KO'},
                    'reponse': {'type': 'string', 'example': 'Not implemented yet'}
                }
            }
        }
    }
})
def get_canal_top_activity(channel_name):
    raise Exception("Not implemented yet")

@canal_bp.route("/channel", methods=["POST"])
@swag_from({
    'tags': ['Canaux'],
    'summary': 'Créer un nouveau canal',
    'description': 'Crée un nouveau canal avec un nom et un statut privé/public',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'description': 'Nom du canal', 'example': 'general'},
                    'private': {'type': 'boolean', 'description': 'Canal privé ou public', 'example': False}
                },
                'required': ['name', 'private']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Canal créé avec succès',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'OK'},
                    'reponse': {'type': 'string', 'description': 'Informations du canal créé'}
                }
            }
        },
        500: {
            'description': 'Erreur lors de la création',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'KO'},
                    'reponse': {'type': 'string', 'description': 'Message d\'erreur'}
                }
            }
        }
    }
})
def create_canal():
    try:
        data = request.get_json()
        canal = canal_repository.create_canal(data.get("name"),data.get("private"))
        return jsonify({'status': "OK", 'reponse': str(canal)})
    except Exception as e:
        return jsonify({'status': "KO", 'reponse': str(e)})

@canal_bp.route("/channel/<name>/topic", methods=["POST"])
@swag_from({
    'tags': ['Canaux'],
    'summary': 'Mettre à jour le topic d\'un canal',
    'description': 'Met à jour le sujet/topic d\'un canal spécifique',
    'parameters': [
        {
            'name': 'name',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Nom du canal'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'topic': {'type': 'string', 'description': 'Nouveau topic du canal', 'example': 'Discussion générale'}
                },
                'required': ['topic']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Topic mis à jour avec succès',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'OK'},
                    'reponse': {'type': 'string', 'example': 'Le topic a ete mis a jour'}
                }
            }
        },
        500: {
            'description': 'Erreur lors de la mise à jour',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'KO'},
                    'reponse': {'type': 'string', 'description': 'Message d\'erreur'}
                }
            }
        }
    }
})
def update_canal_topic(name):
    try:
        body = request.get_json()
        topic = body.get("topic")
        content = canal_repository.update_canal_topic(name, topic)
        return jsonify({'status': "OK", 'reponse': "Le topic a ete mis a jour"})
    except Exception as e:
        return jsonify({'status': "KO", 'reponse': str(e)})

@canal_bp.route("/channel/<name>/mode", methods=["POST"])
@swag_from({
    'tags': ['Canaux'],
    'summary': 'Mettre à jour le mode d\'un canal',
    'description': 'Met à jour le mode d\'un canal (lecture/écriture et privé/public)',
    'parameters': [
        {
            'name': 'name',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Nom du canal'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'mode': {
                        'type': 'string', 
                        'description': 'Mode du canal (r/w pour lecture/écriture, +/- pour public/privé)', 
                        'example': 'w+',
                        'pattern': '^[rw][+-]$'
                    }
                },
                'required': ['mode']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Mode mis à jour avec succès',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'OK'},
                    'reponse': {'type': 'string', 'example': 'Le mode a ete mis a jour'}
                }
            }
        },
        500: {
            'description': 'Erreur lors de la mise à jour ou mode invalide',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'KO'},
                    'reponse': {'type': 'string', 'description': 'Message d\'erreur'}
                }
            }
        }
    }
})
def update_canal_mode(name):
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
    'tags': ['Utilisateurs'],
    'summary': 'Inviter un utilisateur dans un canal',
    'description': 'Invite un utilisateur dans un canal (seuls les modérateurs et propriétaires peuvent inviter)',
    'parameters': [
        {
            'name': 'name',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Nom du canal'
        },
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Token JWT d\'authentification'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'pseudo': {'type': 'string', 'description': 'Pseudo de l\'utilisateur à inviter', 'example': 'roger'}
                },
                'required': ['pseudo']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Utilisateur invité avec succès',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'OK'},
                    'reponse': {'type': 'string', 'example': 'User invited to channel general'}
                }
            }
        },
        403: {
            'description': 'Non autorisé à inviter des utilisateurs',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'KO'},
                    'reponse': {'type': 'string', 'example': 'You are not authorized to invite users to this channel'}
                }
            }
        },
        500: {
            'description': 'Erreur serveur',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'KO'},
                    'reponse': {'type': 'string', 'description': 'Message d\'erreur'}
                }
            }
        }
    }
})
def invite_user_to_canal(channel_name):
    """
        inviter un utilisateur
    — Payload : { "pseudo": "roger" }
    — Vérifier que seul un modérateur ou owner peut inviter un utilisateur
    """
    headers = dict(request.headers)
    token = headers.get("Authorization", None)
    decoded = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])
    decoded.pseudo
    role = role_repository.get_user_roles(channel_name, decoded.pseudo)
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
    'tags': ['Utilisateurs'],
    'summary': 'Bannir un utilisateur d\'un canal',
    'description': 'Bannit un utilisateur d\'un canal (seuls les propriétaires peuvent bannir)',
    'parameters': [
        {
            'name': 'name',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Nom du canal'
        },
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Token JWT d\'authentification'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'pseudo': {'type': 'string', 'description': 'Pseudo de l\'utilisateur à bannir', 'example': 'roger'},
                    'banned_reason': {'type': 'string', 'description': 'Raison du bannissement', 'example': 'Comportement inapproprié'}
                },
                'required': ['pseudo']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Utilisateur banni avec succès',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'OK'},
                    'reponse': {'type': 'string', 'example': 'User invited to channel general'}
                }
            }
        },
        403: {
            'description': 'Non autorisé à bannir des utilisateurs',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'KO'},
                    'reponse': {'type': 'string', 'example': 'You are not authorized to invite users to this channel'}
                }
            }
        },
        500: {
            'description': 'Erreur serveur',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'KO'},
                    'reponse': {'type': 'string', 'description': 'Message d\'erreur'}
                }
            }
        }
    }
})
def ban_user_from_channel(channel_name):
    """
        bannir un utilisateur
    — Payload : { "pseudo": "roger", "banned_reason": "optional reason" }
    — Vérifier que seul un owner peut bannir un utilisateur
    """
    headers = dict(request.headers)
    token = headers.get("Authorization", None)
    decoded = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])
    decoded.pseudo
    role = role_repository.get_user_roles(channel_name, decoded.pseudo)
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
    'tags': ['Canaux'],
    'summary': 'Modifier un canal',
    'description': 'Met à jour le topic et le mode d\'un canal en une seule opération',
    'parameters': [
        {
            'name': 'name',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Nom du canal'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'topic': {'type': 'string', 'description': 'Nouveau topic du canal', 'example': 'Discussion générale'},
                    'mode': {
                        'type': 'string', 
                        'description': 'Mode du canal (r/w pour lecture/écriture, +/- pour public/privé)', 
                        'example': 'w+',
                        'pattern': '^[rw][+-]$'
                    }
                },
                'required': ['topic', 'mode']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Canal mis à jour avec succès',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'OK'},
                    'reponse': {'type': 'string', 'example': 'Canal mis a jour'}
                }
            }
        },
        500: {
            'description': 'Erreur lors de la mise à jour',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'KO'},
                    'reponse': {'type': 'string', 'description': 'Message d\'erreur'}
                }
            }
        }
    }
})
def modify_canal(name):
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
    'tags': ['Canaux'],
    'summary': 'Supprimer un canal',
    'description': 'Supprime définitivement un canal',
    'parameters': [
        {
            'name': 'canal_nom',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Nom du canal à supprimer'
        }
    ],
    'responses': {
        200: {
            'description': 'Canal supprimé avec succès',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'OK'},
                    'reponse': {'type': 'string', 'description': 'Informations du canal supprimé'}
                }
            }
        },
        500: {
            'description': 'Erreur lors de la suppression',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'KO'},
                    'reponse': {'type': 'string', 'description': 'Message d\'erreur'}
                }
            }
        }
    }
})
def delete_canal(canal_nom):
    try:
        canal = canal_repository.del_canal(canal_nom)
        return jsonify({'status': "OK", 'reponse': str(canal)})
    except Exception as e:
        return jsonify({'status': "KO", 'reponse': str(e)})
