from flask import Blueprint, jsonify, request
from repositories import canal_repository
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
def get_canal_users(channel_name):
    raise Exception("Not implemented yet")

@canal_bp.route("/channel/<name>/config", methods=["GET"])
def get_canal_config(channel_name):
    raise Exception("Not implemented yet")

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
def update_canal_topic(channel_name):
    raise Exception("Not implemented yet")

@canal_bp.route("/channel/<name>/mode", methods=["POST"])
def update_canal_mode(channel_name):
    raise Exception("Not implemented yet")

@canal_bp.route("/channel/<name>/invite", methods=["POST"])
def invite_user_to_channel(channel_name):
    raise Exception("Not implemented yet")

@canal_bp.route("/channel/<name>/ban", methods=["POST"])
def ban_user_from_channel(channel_name):
    raise Exception("Not implemented yet")

@canal_bp.route("/channel/<name>", methods=["PATCH"])
def modify_chanel(channel_name):
    raise Exception("Not implemented yet")

@canal_bp.route("/channel/<canal_nom>", methods=["DELETE"])
def delete_canal(canal_nom):
    try:
        canal_repository.del_canal(canal_nom)
        return jsonify({'status': "OK", 'reponse': "Canal "+ canal_nom + " a ete supprime"})
    except Exception as e:
        return jsonify({'status': "KO", 'message': str(e)})

