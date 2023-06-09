from flask import Flask

from config import Config
from flask_cors import CORS
from app.routes import api_routes
from flask_jwt_extended import JWTManager
from app.models import db
from .tasks.file.tasks import scheduler

app = Flask(__name__)
app.config.from_object(Config)
app_context = app.app_context()
app_context.push()
cors = CORS(app)
jwt = JWTManager(app)
db.init_app(app)
db.create_all()
#app.register_blueprint(errors_scope, url_prefix="/")

app.register_blueprint(api_routes, url_prefix='/api')

#with app.app_context():
#    scheduler.start()
