from flask import Blueprint, request, send_file
from app.controllers.file import get_detail
from app.models import File
from flask_jwt_extended import jwt_required
from io import BytesIO
from app.validators.file import validate_get_file
from app.data_transfer_objects.file import FileTypeDTO
from app.enums.file import FileTypeEnum
from app.database import db

api_routes = Blueprint('api', __name__)


@api_routes.route('/files/<int:file_id>', methods=['GET'])
# @jwt_required()
def get_file(file_id: int):
    file_type = FileTypeDTO(request.args.get('type'))
    validate_get_file(file_type)
    fetched_file = get_detail(File(id=file_id))
    if file_type.file_type == FileTypeEnum.ORIGINAL.value:
        return send_file(BytesIO(fetched_file.original_data), download_name=fetched_file.original_name), 200
    if file_type.file_type == FileTypeEnum.COMPRESSED.value:
        return send_file(BytesIO(fetched_file.compressed_data), download_name=fetched_file.compressed_name), 200


@api_routes.route('/create', methods=['POST'])
def create_file():
    # create
    file = request.files['file']
    file_name = file.filename
    file_data = file.read()
    file_to_save = File(original_name=file_name, original_data=file_data)
    db.session.add(file_to_save)
    db.session.commit()

    # compress
    fetched_file = File.query.get_or_404(file_to_save.id)

    # upload
    fetched_file.compressed_name = fetched_file.original_name.split('.')[0] + '.tar.gz'
    fetched_file.compressed_data = tar_file_data
    db.session.commit()

    return {'id': file_to_save.id}, 200
