from app.models.models import File
from .i_File import IFile
from app.exceptions import FileNotFound


class DatabaseFileStorage(IFile):
    @classmethod
    def extract_name(cls, file):
        return file.original_name, file.original_data

    def get(self, file_id) -> tuple:
        fetched_file = File.query.get_or_404(file_id)
        name, data = self.extract_name(fetched_file)
        return data, name

    def save(self, file_name, file_data, new_format) -> int:
        try:
            fetched_file = File.query.get_or_404(id)
            fetched_file.compressed_name = file_name.compressed_name
            fetched_file.compressed_data = file_data.compressed_data
            return fetched_file
        except Exception as ex:
            raise FileNotFound(ex)
