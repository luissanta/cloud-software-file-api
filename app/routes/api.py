from flask import Blueprint, request, send_file
from app.controllers.file import get_detail
from app.tasks.file import converter_request
from app.models import File, db
from flask_jwt_extended import jwt_required
from io import BytesIO
from app.validators.file import validate_get_file
from app.data_transfer_objects.file import FileTypeDTO
from app.enums.file import FileTypeEnum

api_routes = Blueprint('api', __name__)


@api_routes.route('/files/<int:_id>', methods=['GET'])
# @jwt_required()
def get_file(_id: int):
    file_type = FileTypeDTO(request.args.get('type'))
    validate_get_file(file_type)
    fetched_file = get_detail(File(id=_id))
    if file_type.file_type == FileTypeEnum.ORIGINAL.value:
        return send_file(BytesIO(fetched_file.original_data), download_name=fetched_file.original_name), 200
    if file_type.file_type == FileTypeEnum.COMPRESSED.value:
        archivo = File.query.filter_by(id=_id).first()
        return send_file(BytesIO(archivo.compressed_data), download_name='archivo.gz', as_attachment=True)


@api_routes.route('/queue/<int:file_id>', methods=['GET'])
def queue(file_id: int):
    converter_request.apply_async(args=(2, file_id, 'gz'), queue='request')
    return {}, 200


@api_routes.route('/test', methods=['POST'])
def test():
    name = request.files['file'].filename
    data = request.files['file'].read()
    new_file = File(original_name=name, original_data=data)
    db.session.add(new_file)
    db.session.commit()
    return {'id': new_file.id}, 200


@api_routes.route('/test_c', methods=['POST'])
def test_c():
    return {'mensaje': 'Archivo zip guardado correctamente'}
