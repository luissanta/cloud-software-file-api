from app.repositories import get_detail_by_id
from app.models import File


def get_detail(file: File) -> File:
    return get_detail_by_id(file)
