from wsgi import app
from flask_restful import Api


api = Api(app)

from .send_file import SendFile

api.add_resource(SendFile, '/api/sales/import/file')