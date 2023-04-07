from flask import Blueprint
from app.controller import get_detail
from app.tasks import converter_request
from app.models import File

api_routes = Blueprint('api', __name__)


@api_routes.route('/files/<int:_id>', methods=['GET'])
# @jwt_required()
def get_file(_id: int):
    file_to_get = File(id=_id)
    fetched_file = get_detail(file_to_get)
    return fetched_file, 200


# todo: solo para validar la queue
@api_routes.route('/queue/<file_id>', methods=['GET'])
def queue(file_id: str):
    task_id = 2
    args = (task_id, file_id,)
    converter_request.apply_async(args=args, queue='request')
    # return get_detail(file_id), 200
