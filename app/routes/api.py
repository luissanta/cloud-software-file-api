from flask import Blueprint, request, send_file
from app.controllers.file import get_detail
from app.tasks.file import converter_request
from app.models import File, db
from flask_jwt_extended import jwt_required
import io

api_routes = Blueprint('api', __name__)


@api_routes.route('/files/<int:_id>', methods=['GET'])
@jwt_required()
def get_file(_id: int):
    fetched_file = get_detail(File(id=_id))
    return send_file(io.BytesIO(fetched_file.original_data), download_name=fetched_file.original_name), 200


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
    archivo = request.files['file']
    nombre_archivo = archivo.filename

    print(nombre_archivo)
    # Renombrar el archivo para eliminar caracteres no válidos
    # nombre_archivo = nombre_archivo.replace('\0', '').replace('/', '_').replace('\\', '_')
    #
    # # Crear un buffer de memoria para almacenar el archivo comprimido
    # buffer = io.BytesIO()
    #
    # # Comprimir el archivo y guardar en el buffer de memoria
    # with zipfile.ZipFile(buffer, 'w') as zip_ref:
    #     zip_ref.write(archivo.read(), nombre_archivo)
    #
    # # Obtener los datos del archivo comprimido como bytes
    #
    # datos_comprimidos = buffer.getvalue()
    #
    # new_file = File(original_name='fds', original_data=datos_comprimidos, compressed_name='hola.gz', compressed_data=datos_comprimidos)
    # db.session.add(new_file)
    # db.session.commit()
    return {}, 200
