from io import BytesIO
from app.helpers.compressors.i_file_compressor import IFileCompressor
import tarfile


class TarBz2Compressor(IFileCompressor):
    def compress(self, file_data: bytes, file_name: str) -> tuple:
        with BytesIO() as buffer:
            with tarfile.open(fileobj=buffer, mode='w:bz2') as tar_file:
                tar_info = tarfile.TarInfo(file_name)
                tar_info.size = len(file_data)
                tar_file.addfile(tar_info, BytesIO(file_data))

            buffer.seek(0)
            tar_bz2_file_data = buffer.read()

        gz_file_name = self.compressed_name(file_name)
        return tar_bz2_file_data, gz_file_name

    def compressed_name(self, file_name: str) -> str:
        name = file_name.split('.')
        return name[0] + '.tar.bz2'
