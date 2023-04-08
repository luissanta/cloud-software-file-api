from app.models import db, File, FileSchema
from app.exceptions import FileNotFound

file_schema = FileSchema()


def get_detail_by_id(file: File) -> File:
    try:
        file_to_get = File.query.get_or_404(file.id)
        return file_to_get
    except Exception as ex:
        raise FileNotFound(ex)


def update(file_to_update: File) -> file_schema:
    try:
        file = File.query.get_or_404(file_to_update.id)
        file = file_to_update
        db.session.commit()
        return file_schema.dump(file)
    except Exception as ex:
        return {'message': str(ex)}, 500
