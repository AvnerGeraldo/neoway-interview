from wsgi import app
from flask_restful import Api


api = Api(app)
from . import send_file as fileRoute, status_file as statusRoute

api.add_resource(fileRoute.SendFile, '/api/sales/import/file')
api.add_resource(statusRoute.StatusFile, '/api/sales/import/<int:file_id>/status')