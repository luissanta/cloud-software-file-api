from app.repositories import get
from app.models import File, FileSchema


def get_detail(file: File) -> FileSchema:
    return get(file)
