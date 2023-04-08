from app.models import db, File
from app.exceptions import FileNotFound


def get_detail_by_id(file: File) -> File:
    try:
        return File.query.get_or_404(file.id)
    except Exception as ex:
        raise FileNotFound(ex)


def update(file_to_update: File) -> File | Exception:
    try:
        file = File.query.get_or_404(file_to_update.id)
        print('ll')
        file = file_to_update
        db.session.commit()
        return file
    except Exception as ex:
        return ex
