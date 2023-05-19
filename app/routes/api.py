import logging.config
import json
from flask import Blueprint, request

import base64

from .pusub_topic import PubSubTopic
from ..utils.file_converter import FileConverter

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

api_routes = Blueprint('api', __name__)
file_converter = FileConverter()



@api_routes.route('/files/process', methods=['POST'])
def create_task():
    pubSub = PubSubTopic()
    try:
        pubSub.send_message(request.data.decode())

        data = json.loads(request.data)

        pubSub.send_message(data)

        message =json.loads(base64.b64decode(data['message']['data']).decode('utf-8'))

        pubSub.send_message(message)

        file_converter.converter_request(message["task_id"], message["url"], message["new_format"])

        pubSub.send_message(request.data)
        print(request)
        return request.data, 200
    except Exception as e:
        pubSub.send_message(e.args[0])
        logger.error("error processing message: error {error}".format(error=e))
        return {"error": e}, 501


