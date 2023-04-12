from abc import ABC, abstractmethod
from app.enums.file import FileConverterEnum
from app.helpers.compressors.formats import TarGzCompressor, ZipCompressor, TarBz2Compressor
from app.exceptions import UnsupportedFileConverter


class Compressor(ABC):
    @abstractmethod
    def compress(self) -> TarGzCompressor | ZipCompressor | TarBz2Compressor:
        pass


class TarGz(Compressor):
    def compress(self) -> TarGzCompressor:
        return TarGzCompressor()


class TarBz2(Compressor):
    def compress(self) -> TarBz2Compressor:
        return TarBz2Compressor()


class Zip(Compressor):
    def compress(self) -> ZipCompressor:
        return ZipCompressor()


class CompressorFactory:
    @staticmethod
    def get_compressor(compress_type: str):
        if compress_type == FileConverterEnum.TAR_GZ.value:
            return TarGz().compress()
        elif compress_type == FileConverterEnum.ZIP.value:
            return Zip().compress()
        elif compress_type == FileConverterEnum.TAR_BZ2.value:
            return TarBz2().compress()
        else:
            raise UnsupportedFileConverter('The extension converter is not supported')
