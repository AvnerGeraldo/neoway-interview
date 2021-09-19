from helpers.db import updateModel
from flask import abort
from database.types import StatusEnum
from database.models import SaleFile, Log
from worker import conn
from rq.job import Job

class StatusImportFile():
    def getStatus(self, saleFileId: int):
        if not type(saleFileId) is int:
            abort('O ID informado é inválido. Por favor entre em contato com o administrador.', 406)

        saleFile = SaleFile.query.filter_by(id=saleFileId).first()

        if not saleFile:
            abort('Dados do arquivo não encontrados.', 204)

        fileStatus = saleFile.status.value
        jobId = saleFile.job_id

        logList = Log.query.filter_by(sale_file_id=saleFileId)

        output = self.__formatOutputStatus(fileStatus, jobId, logList)
        jobStatus = (output['job_status']).lower()

        if jobStatus not in ['started']:
            hasSaleFile = SaleFile.query.filter_by(job_id=jobId)
            if hasSaleFile:
                updateModel(hasSaleFile, dict(status=self.__getStatusEnum(jobStatus)))
        
        return output

    def __getStatusEnum(self, jobStatus: str):
        try:
            return {
                'canceled': StatusEnum.canceled,
                'failed': StatusEnum.failed,
                'not found': StatusEnum.error,
                'started': StatusEnum.processing,
                'finished': StatusEnum.completed
            }[jobStatus]
        except:
            return StatusEnum.error

    def __formatOutputStatus(self, fileStatus: str, jobId: str, logsFromDb: list):
        jobStatus = ''
        
        if jobId:
            try:
                job = Job.fetch(jobId, connection=conn)
                jobStatus = 'started'

                if job.is_finished:
                    jobStatus = 'finished'

                if job.is_failed or job.is_deferred:
                    jobStatus = 'failed'

                if job.is_canceled:
                    jobStatus = 'canceled'
            except Exception as error:
                jobStatus = 'not found'

        return {
            'status': str(fileStatus),
            'job_status': jobStatus,
            'logs': ['%s - %s' % (
                log.created_at.strftime('%Y-%m-%d %H:%M:%S'), 
                log.message
                ) for log in logsFromDb]
        }