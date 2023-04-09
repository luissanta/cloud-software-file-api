from app.data_transfer_objects.file import FileTypeDTO
from app.exceptions import QueryParamsRequired


def validate_get_file(file_type: FileTypeDTO) -> None:
    if not file_type.file_type:
        raise QueryParamsRequired('The type parameters is required')
