from io import BytesIO
import gzip


def compress_to_gz(file_data: bytes, file_name: str) -> tuple:
    with BytesIO() as buffer:
        with gzip.GzipFile(fileobj=buffer, mode='wb', filename=file_name) as gz_file:
            gz_file.write(file_data)

        buffer.seek(0)
        gz_file_data = buffer.read()

    gz_file_name = get_name_compressed(file_name)
    return gz_file_data, gz_file_name


def get_name_compressed(file_name: str) -> str:
    name = file_name.split('.')
    return name[0] + '.gz'
