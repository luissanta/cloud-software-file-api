from app.data_transfer_objects.file import FileTypeDTO
from app.exceptions import QueryParamsRequired, UnsupportedQueryParam
from app.enums.file import FileTypeEnum


def validate_get_file(file_type: FileTypeDTO) -> None:
    if not file_type.file_type:
        raise QueryParamsRequired('The type parameters is required')

    formats = [file_type.value for file_type in FileTypeEnum.__members__.values()]

    if file_type.file_type not in formats:
        raise UnsupportedQueryParam('The parameter is not supported')
