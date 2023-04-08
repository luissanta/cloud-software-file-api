from app.services.file import FileServiceI
from app.models import File
from app.repositories.file import get_detail_by_id


class FileServiceImpl(FileServiceI):
    def __init__(self) -> None:
        super().__init__()

    def get_detail_by_id(self, file: File) -> File:
        return get_detail_by_id(file)
