from app.models import db, File
from app.exceptions import FileNotFound


def get_detail_by_id(file: File) -> File:
    try:
        return File.query.get(file.id)
    except Exception as ex:
        raise FileNotFound(ex)


def update(file_to_update: File) -> File | Exception:
    try:
        fetched_file = get_detail_by_id(file_to_update)
        fetched_file.compressed_name = file_to_update.compressed_name
        fetched_file.compressed_data = file_to_update.compressed_data
        db.session.commit()
        return fetched_file
    except Exception as ex:
        return ex
