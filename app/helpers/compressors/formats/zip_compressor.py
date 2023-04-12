from io import BytesIO
import zipfile
from app.helpers.compressors.i_file_compressor import IFileCompressor


class ZipCompressor(IFileCompressor):
    def compress(self, file_data: bytes, file_name: str) -> tuple:
        with BytesIO() as buffer:
            with zipfile.ZipFile(file=buffer, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
                zip_info = zipfile.ZipInfo(file_name)
                zip_file.writestr(zip_info, file_data)

            buffer.seek(0)
            zip_file_data = buffer.read()

        zip_file_name = self.compressed_name(file_name)
        return zip_file_data, zip_file_name

    def compressed_name(self, file_name: str) -> str:
        name = file_name.split('.')
        return name[0] + '.zip'
