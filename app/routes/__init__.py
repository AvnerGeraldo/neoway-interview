from wsgi import app
from flask_restful import Api


api = Api(app)

from resources import send_file

api.add_resource(send_file.SendFile, '/api/sales/import/file')