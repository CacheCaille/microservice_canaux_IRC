from flask import Blueprint, jsonify, request
from repositories import canal_repository

canal_bp = Blueprint("main", __name__)

@canal_bp.route("/channel", methods=["GET"])
def get_canals():
    try:
        content = canal_repository.get_canals()
        return jsonify({'status': "OK", 'reponse': content})
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
def create_chanel(channel_name):
    raise Exception("Not implemented yet")

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

@canal_bp.route("/channel/<name>", methods=["DELETE"])
def delete_chanel(channel_name):
    raise Exception("Not implemented yet")