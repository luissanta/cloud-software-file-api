from abc import ABC, abstractmethod
from app.enums.file import FileConverterEnum
from app.helpers.compressors.formats import GzCompressor, ZipCompressor
from app.exceptions import UnsupportedFileConverter


class Compressor(ABC):
    @abstractmethod
    def compress(self):
        pass


class Gz(Compressor):
    def compress(self) -> GzCompressor:
        return GzCompressor()


class Zip(Compressor):
    def compress(self) -> ZipCompressor:
        return ZipCompressor()


class CompressorFactory:
    @staticmethod
    def compress_file(compress_type: str):
        if compress_type == FileConverterEnum.GZ.value:
            return Gz().compress()
        elif compress_type == FileConverterEnum.ZIP.value:
            return Zip().compress()
        else:
            raise UnsupportedFileConverter('The extension converter is not supported')
