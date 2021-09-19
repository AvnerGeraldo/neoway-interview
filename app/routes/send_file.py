from flask import request, make_response, jsonify, abort
from flask_restful import Resource
from wsgi import app

from database.models import SaleFile
from database.redis import q
from database.types import StatusEnum
from controllers.file_task import FileTask

def queueTask(func, rows):
    with app.app_context():
        func(rows)

class SendFile(Resource):
    def post(self):
        try:
            if self.__validateRequest(request):
                rawData = request.get_data()
                rows = rawData.decode().splitlines(False)

            if len(rows) <= 1:
                abort('Arquivo vazio', 406)

            FileTaskInstance = FileTask()
            FileTaskInstance.createSaleFile()

            nextId = FileTaskInstance.saleId
            statusLink = '/api/sales/import/%s/status' % nextId

            job = q.enqueue_call(func=queueTask, args=(FileTaskInstance.handle, rows, ), result_ttl=3600, timeout=900)
            FileTaskInstance.setSaleFileStatus(StatusEnum.processing, job.get_id())

            return make_response(jsonify({
                "message": 'Arquivo enviado com sucesso! Logo iremos processá-lo. Por favor, verique seu status em %s' % statusLink
            }), 200)
        except Exception as error:
            if hasattr(error, 'code'):
                return make_response(jsonify({
                    "message": error.description
                }), error.code)

            return make_response(jsonify({
                "message": str(error)
            }), 400)


    def __validateRequest(self, request) -> bool:
        contentTypeHeader = request.headers.get('content-type')
        contentLengthHeader = request.headers.get('content-length')
        acceptHeader = request.headers.get('accept')
        allowedContentTypes = ['text/plain']
        limitSize = 100 * 1024 * 1024 # 100 MB

        if not contentTypeHeader or contentTypeHeader.lower() not in allowedContentTypes:
            abort(400, 'Requisição não permitida para este tipo de conteúdo')

        if int(contentLengthHeader) > limitSize:
            abort(203, 'O tamanho do arquivo é muito grande para ser processado.')

        if not acceptHeader or acceptHeader.lower() not in allowedContentTypes:
            abort(406, 'Requisição não permitida para este tipo de conteúdo na tag \'accept\'')

        return True