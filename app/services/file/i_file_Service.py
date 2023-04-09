from app.models import File
from abc import ABC, abstractmethod


class IFileService(ABC):
    @abstractmethod
    def get_detail_by_id(self, file: File) -> File:
        pass
