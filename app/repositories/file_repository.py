from app.models import db, File, FileSchema
from app.exceptions import FileNotFound

file_schema = FileSchema()


def get(file: File) -> file_schema:
    try:
        file_to_get = File.query.get_or_404(file.id)
        return file_schema.dump(file_to_get)
    except Exception as ex:
        raise FileNotFound(ex)


def update(file_to_update: File) -> file_schema:
    try:
        file_update = File.query.get_or_404(file_to_update.id)
        file_update.detail = file_to_update.detail
        db.session.commit()
        return file_schema.dump(file_update)
    except Exception as ex:
        return {'message': str(ex)}, 500
