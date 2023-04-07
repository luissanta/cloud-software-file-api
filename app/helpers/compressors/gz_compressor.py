import zlib


def compress_gz(file):
    data = file.read()
    file_gz = zlib.compress(data)
    return file_gz
