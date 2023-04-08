import zipfile


def compress_to_zip(file, file_name: str) -> tuple:
    zip_file = zipfile.ZipFile('archivo.zip', mode='w')
    zip_file.write(file)
    zip_file.close()

    with open('archivo.zip', 'rb') as f:
        zip_file_data = f.read()
    zip_file_name = get_name_compressed(file_name)
    return zip_file_data, zip_file_name


def get_name_compressed(file_name: str) -> str:
    name = file_name.split('.')
    return name[0] + '.zip'
