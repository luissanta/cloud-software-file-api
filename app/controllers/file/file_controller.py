from app.models import File
from app.services.file.impl import FileServiceImpl


def get_detail(file: File) -> File:
    file_service_i = FileServiceImpl()
    return file_service_i.get_detail_by_id(file)
