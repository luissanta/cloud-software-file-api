import gzip


def compress_to_gz(file_data: bytes, file_name: str) -> tuple:
    gz_file_data = gzip.compress(file_data)
    gz_file_name = get_name_compressed(file_name)
    return gz_file_data, gz_file_name


def get_name_compressed(file_name: str) -> str:
    name = file_name.split('.')
    return name[0] + '.gz'
