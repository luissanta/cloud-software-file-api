from flask import Blueprint, request, send_file
from app.controllers.file import get_detail
from app.models import File
from flask_jwt_extended import jwt_required
from io import BytesIO
from app.validators.file import validate_get_file
from app.data_transfer_objects.file import FileTypeDTO
from app.enums.file import FileTypeEnum

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
