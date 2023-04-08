from flask import Blueprint, request, send_file, Response
from app.controllers.file import get_detail
from app.tasks.file import converter_request
from app.models import File, db
from flask_jwt_extended import jwt_required
import io
from app.validators.file import validate_get_file
from app.data_transfer_objects.file import FileTypeDTO
from app.enums.file import FileTypeEnum
import gzip

api_routes = Blueprint('api', __name__)


@api_routes.route('/files/<int:_id>', methods=['GET'])
# @jwt_required()
def get_file(_id: int):
    file_type = FileTypeDTO(request.args.get('type'))
    validate_get_file(file_type)
    fetched_file = get_detail(File(id=_id))
    if file_type.file_type == FileTypeEnum.ORIGINAL.value:
        return send_file(io.BytesIO(fetched_file.original_data), download_name=fetched_file.original_name), 200
    if file_type.file_type == FileTypeEnum.COMPRESSED.value:
        archivo = File.query.filter_by(id=_id).first()
        return send_file(io.BytesIO(archivo.compressed_data), download_name='archivo.gz', as_attachment=True)


@api_routes.route('/queue/<int:file_id>', methods=['GET'])
def queue(file_id: int):
    task_id = 2
    new_format = 'gz'
    args = (task_id, file_id, new_format)
    print(args)
    converter_request.apply_async(args=args, queue='request')
    return {}, 200


@api_routes.route('/test', methods=['POST'])
def test():
    file = request.files['file']
    name = file.filename
    data = file.read()
    new_file = File(original_name=name, original_data=data)
    db.session.add(new_file)
    db.session.commit()
    return {'id': new_file.id}, 200


@api_routes.route('/test_c', methods=['POST'])
def test_c():
    import zipfile
    file = request.files['file']
    name = file.filename
    data = file.read()
    new_file = File(original_name=name, original_data=data)
    db.session.add(new_file)
    db.session.commit()

    imagen = File.query.get_or_404(new_file.id)

    with io.BytesIO() as buffer:
        with zipfile.ZipFile(buffer, 'w') as zip:
            zipinfo = zipfile.ZipInfo(imagen.original_name)
            zip.writestr(zipinfo, imagen.original_data)

        buffer.seek(0)
        archivo_zip = buffer.read()

    imagen.compressed_name = 'spam.zip'
    imagen.compressed_data = archivo_zip
    db.session.commit()

    return {'mensaje': 'Archivo zip guardado correctamente'}
