from abc import ABC, abstractmethod


class IFileCompressor(ABC):
    @abstractmethod
    def compress(self, file_data: bytes, file_name: str) -> tuple:
        pass

    @abstractmethod
    def compressed_name(self, file_name: str) -> str:
        pass
