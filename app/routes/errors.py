from flask import jsonify, Blueprint, Response
from app.exceptions import FileNotFound

errors_scope = Blueprint("errors", __name__)


def __generate_error_response(error: Exception) -> Response:
    message = {
        "ErrorType": type(error).__name__,
        "Message": str(error)
    }
    return jsonify(message)


@errors_scope.app_errorhandler(FileNotFound)
def handle_user_not_found(error: FileNotFound) -> Response:
    response = __generate_error_response(error)
    response.status_code = 404
    return response
