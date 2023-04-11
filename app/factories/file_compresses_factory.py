from abc import ABC, abstractmethod
from app.enums.file import FileConverterEnum
from app.helpers.compressors.formats import TarGzCompressor, ZipCompressor
from app.exceptions import UnsupportedFileConverter


class Compressor(ABC):
    @abstractmethod
    def compress(self) -> TarGzCompressor | ZipCompressor:
        pass


class TarGz(Compressor):
    def compress(self) -> TarGzCompressor:
        return TarGzCompressor()


class Zip(Compressor):
    def compress(self) -> ZipCompressor:
        return ZipCompressor()


class CompressorFactory:
    @staticmethod
    def compress_file(compress_type: str):
        if compress_type == FileConverterEnum.TAR_GZ.value:
            return TarGz().compress()
        elif compress_type == FileConverterEnum.ZIP.value:
            return Zip().compress()
        else:
            raise UnsupportedFileConverter('The extension converter is not supported')
