from flask import abort

from . import db

def saveModel(modelInstance):
    try:
        db.session.add(modelInstance)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.close()
        abort(str(e), 500)

def updateModel(modelInstance, updatedData: dict):
    try:
        modelInstance.update(updatedData)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.close()
        abort(str(e), 500)