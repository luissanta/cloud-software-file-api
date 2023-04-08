from app.repositories import get_detail_by_id
from app.models import File, FileSchema


def get_detail(file: File) -> FileSchema:
    return get_detail_by_id(file)
