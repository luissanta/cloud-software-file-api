import logging.config
import json
from flask import Blueprint, request

import base64
from ..utils.file_converter import FileConverter

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

api_routes = Blueprint('api', __name__)
file_converter = FileConverter()


@api_routes.route('/files/process', methods=['POST'])
def create_task():
    try:
        """
        data = json.loads(request.data)
        message =json.loads(base64.b64decode(data['message']['data']).decode('utf-8'))
        file_converter.converter_request(message["task_id"], message["url"], message["new_format"])
        """
        return request.data, 200
    except Exception as e:
        logger.error("error processing message: error {error}".format(error=e))
        return {"error": e}, 501


