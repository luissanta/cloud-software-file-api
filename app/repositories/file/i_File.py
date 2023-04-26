from abc import ABC, abstractmethod


class IFile(ABC):
    @abstractmethod
    def get(self, file_id) -> tuple:
        pass

    @abstractmethod
    def save(self, file_name, file_data, new_format) -> int:
        pass
