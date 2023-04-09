from app.services.file import IFileService
from app.models import File
from app.repositories.file import get_detail_by_id


class FileServiceImpl(IFileService):
    def get_detail_by_id(self, file: File) -> File:
        return get_detail_by_id(file)
