from io import BytesIO
import zipfile


def compress_to_zip(file_data: bytes, file_name: str) -> tuple:
    with BytesIO() as buffer:
        with zipfile.ZipFile(buffer, 'w') as zip_file:
            zip_info = zipfile.ZipInfo(file_name)
            zip_file.writestr(zip_info, file_data)

        buffer.seek(0)
        zip_file_data = buffer.read()

    zip_file_name = get_name_compressed(file_name)
    return zip_file_data, zip_file_name


def get_name_compressed(file_name: str) -> str:
    name = file_name.split('.')
    return name[0] + '.zip'
