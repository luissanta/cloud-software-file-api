from flask import Blueprint, jsonify

api_routes = Blueprint('api', __name__)


@api_routes.route('/files/<filename>', methods=['GET'])
def get_file(filename: str):
    return {}, 200
