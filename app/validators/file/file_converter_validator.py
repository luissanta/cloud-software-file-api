from app.data_transfer_objects.file import FileConverterDTO
from app.exceptions import UnsupportedFileConverter
from app.enums.file import FileConverterEnum


def validate_format_converter(file_converter: FileConverterDTO) -> None:
    formats = [file_converter.value for file_converter in FileConverterEnum.__members__.values()]

    if file_converter.new_format not in formats:
        raise UnsupportedFileConverter('The extension converter is not supported')
