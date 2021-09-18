from flask import request, make_response, jsonify, abort
from flask_restful import Resource

from database.redis import q
from database.models import SaleFile
from database.types import StatusEnum
from controllers.process_file import ProcessFile
from helpers.logger import Logger

def processFileTask(rawData: list):
    nextSaleFileId = SaleFile.getNextId()
    loggerInstance = Logger(nextSaleFileId)
    ProcessFile(loggerInstance).processRawData(rawData)

class SendFile(Resource):
    def post(self):
        try:
            if self.__validateRequest(request):
                rawData = request.get_data()
                rows = rawData.decode().splitlines(False)

            if len(rows) <= 1:
                abort('Arquivo vazio', 406)

            job = q.enqueue_call(func=processFileTask, args=(rows, ), result_ttl=5500, timeout=900)
            addSale = SaleFile(status=StatusEnum.processing, job_id=job.get_id())
            SaleFile.save(addSale)

            return make_response(jsonify({
                "message": 'Arquivo enviado com sucesso! Logo iremos processá-lo'
            }), 200)
        except Exception as error:
            return make_response(jsonify({
                "message": error.description
            }), error.code)


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