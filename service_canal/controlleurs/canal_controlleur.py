from flask import Blueprint, jsonify, request
from repositories import canal_repository
from repositories import role_repository
from service_canal.app import db
import jwt
import json 
canal_bp = Blueprint("main", __name__)

@canal_bp.route("/channel", methods=["GET"])
def get_canals():
    try:
        content = canal_repository.get_canals()
        return jsonify({'status': "OK", 'reponse': str(content)})
    except Exception as e:
        return jsonify({'status': "KO", 'message': str(e)})

@canal_bp.route("/channel/<name>/users", methods=["GET"])
def get_canal_users(name):
    try:
        users = canal_repository.get_users_by_channel(name)
        return jsonify({'status': "OK", 'users': users})
    except Exception as e:
        return jsonify({'status': "KO", 'message': str(e)})

@canal_bp.route("/channel/<name>/config", methods=["GET"])
def get_canal_config(name):
    try:
        config = canal_repository.get_channel_config(name)
        return jsonify({'status': "OK", 'config': config})
    except Exception as e:
        return jsonify({'status': "KO", 'message': str(e)})

@canal_bp.route("/channel/topActivity", methods=["GET"])
def get_canal_top_activity(channel_name):
    raise Exception("Not implemented yet")

@canal_bp.route("/channel", methods=["POST"])
def create_canal():
    try:
        data = request.get_json()
        canal_repository.create_canal(data.get("name"),data.get("private"))
        return jsonify({'status': "OK", 'reponse': data})
    except Exception as e:
        return jsonify({'status': "KO", 'message': str(e)})

@canal_bp.route("/channel/<name>/topic", methods=["POST"])
def update_canal_topic(name):
    try:
        body = request.get_json()
        topic = body["topic"]
        content = canal_repository.update_canal_topic(name, topic)
        return jsonify({'status': "OK", 'reponse': content})
    except Exception as e:
        return jsonify({'status': "KO", 'message': str(e)})

@canal_bp.route("/channel/<name>/mode", methods=["POST"])
def update_canal_mode(name):
    try:
        body = request.get_json()
        if body.get("mode")[0] == 'r':
            editable = False
        elif body.get("mode")[0] == 'w':
            editable = True

        if body.get("mode")[1] == '+':
            private = False
        elif body.get("mode")[1] == '-':
            private = True

        if editable is None or private is None:
            raise Exception("Le mode ", body.get["mode"], " n'est pas un mode valide")

        content = canal_repository.update_canal_mode(name, editable, private)
        return jsonify({'status': "OK", 'reponse': content})
    except Exception as e:
        return jsonify({'status': "KO", 'message': str(e)})

@canal_bp.route("/channel/<name>/invite", methods=["POST"])
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
        return jsonify({'status': "OK", 'message': f"User invited to channel {channel_name}"})
    else :
        return jsonify({'status': "KO", 'message': "You are not authorized to invite users to this channel"})


@canal_bp.route("/channel/<name>/ban", methods=["POST"])
def ban_user_from_channel(channel_name):
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
    if role == "OWNER":
        # Logic to invite user to channel
        data = request.get_json()
        data.get("pseudo")
        role = role_repository.get_user_roles(channel_name, data.get("pseudo"))
        role.banned_reason = data.get("banned_reason", "No reason provided")
        role.role = "BANNED"
        db.session.commit() # ^^ Il faudrait pas avoir ça là mais on a pas le temp de ce coordonnée pour faire un services
        return jsonify({'status': "OK", 'message': f"User invited to channel {channel_name}"})
    else :
        return jsonify({'status': "KO", 'message': "You are not authorized to invite users to this channel"})

@canal_bp.route("/channel/<name>", methods=["PATCH"])
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
            raise Exception("Le mode ", body.get["mode"], " n'est pas un mode valide")

        content = canal_repository.update_canal_topic(name, topic, editable, private)
        return jsonify({'status': "OK", 'reponse': content})
    except Exception as e:
        return jsonify({'status': "KO", 'message': str(e)})

@canal_bp.route("/channel/<canal_nom>", methods=["DELETE"])
def delete_canal(canal_nom):
    try:
        canal_repository.del_canal(canal_nom)
        return jsonify({'status': "OK", 'reponse': "Canal "+ canal_nom + " a ete supprime"})
    except Exception as e:
        return jsonify({'status': "KO", 'message': str(e)})


@canal_bp.route("/channel/<canal_nom>", methods=["DELETE"])
def delete_canal(canal_nom):
    try:
        canal_repository.del_canal(canal_nom)
        return jsonify({'status': "OK", 'reponse': "Canal "+ canal_nom + " a ete supprime"})
    except Exception as e:
        return jsonify({'status': "KO", 'message': str(e)})

