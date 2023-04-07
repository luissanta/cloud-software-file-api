from flask import Response
import zlib


def compress_gz(file):
    data = file.read()
    compressed_data = zlib.compress(data)
    gz_file = Response(compressed_data, mimetype='application/octet-stream')
    gz_file.headers['Content-Disposition'] = 'attachment; filename=file.gz'
    return gz_file
