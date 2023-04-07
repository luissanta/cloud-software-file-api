from flask import Blueprint, request
from app.controller import get_by_file_name
from app.tasks import converter_request
from flask_jwt_extended import jwt_required

api_routes = Blueprint('api', __name__)


@api_routes.route('/files/<filename>', methods=['GET'])
@jwt_required()
def get_file(filename: str):
    return get_by_file_name(filename), 200


# todo: solo para validar la queue
@api_routes.route('/queue/<filename>', methods=['GET'])
def queue(filename: str):
    args = (filename,)
    converter_request.apply_async(args=args, queue='request')
    return get_by_file_name(filename), 200
