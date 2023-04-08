from flask import Blueprint, request, send_file
from app.controllers.file import get_detail
from app.tasks.file import converter_request
from app.models import File, db
import io

api_routes = Blueprint('api', __name__)


@api_routes.route('/files/<int:_id>', methods=['GET'])
# @jwt_required()
def get_file(_id: int):
    fetched_file = get_detail(File(id=_id))
    return send_file(io.BytesIO(fetched_file.original_data), download_name=fetched_file.original_name), 200


# todo: solo para validar la queue
@api_routes.route('/queue/<int:file_id>', methods=['GET'])
def queue(file_id: int):
    task_id = 2
    new_format = 'gz'
    args = (task_id, file_id, new_format)
    print(args)
    converter_request.apply_async(args=args, queue='request')
    return {}, 200


# todo: solo para validar la queue
@api_routes.route('/test', methods=['POST'])
def test():
    file = request.files['file']
    name = file.filename
    data = file.read()
    new_file = File(original_name=name, original_data=data)
    db.session.add(new_file)
    db.session.commit()
    return {'id': new_file.id}, 200
