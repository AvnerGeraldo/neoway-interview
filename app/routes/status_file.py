from flask import make_response, jsonify
from flask_restful import Resource
from controllers.status_import_file import StatusImportFile

class StatusFile(Resource):
    def get(self, file_id):
        try:
            res = StatusImportFile().getStatus(file_id)
            return make_response(jsonify(res), 200)
        except Exception as error:
            if hasattr(error, 'code'):
                return make_response(jsonify({
                    "message": error.description
                }), error.code)

            return make_response(jsonify({
                "message": str(error)
            }), 400)