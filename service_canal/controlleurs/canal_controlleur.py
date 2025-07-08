from flask import Blueprint, jsonify
from flask import request
from repositories import canal_repository

canal_bp = Blueprint("main", __name__)

@canal_bp.route("/channel", methods=["GET"])
def get_canals():
    return canal_repository.get_canals()

@canal_bp.route("/channel/<name>/users", methods=["GET"])
def get_canal_users(channel_name):
    raise Exception("Not implemented yet")

@canal_bp.route("/channel/<name>/config", methods=["GET"])
def get_canal_config(channel_name):
    raise Exception("Not implemented yet")

@canal_bp.route("/channel", methods=["POST"])
def create_chanel(channel_name):
    raise Exception("Not implemented yet")

@canal_bp.route("/channel/<name>/topic", methods=["POST"])
def update_canal_topic(channel_name):
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