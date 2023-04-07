from flask import Response
import zipfile


def compress_zip(file):
    zip_file = zipfile.ZipFile('archivo.zip', mode='w')
    zip_file.write(file)
    zip_file.close()

    with open('archivo.zip', 'rb') as f:
        data = f.read()

    response = Response(data, mimetype='application/zip')
    response.headers['Content-Disposition'] = 'attachment; filename=archivo.zip'
    return response