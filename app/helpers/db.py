from flask import abort
from sqlalchemy import func
from database import db

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

def bulkModel(objects):
    try:
        db.session.bulk_save_objects(objects)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.close()
        abort(str(e))

def getNextId(model):
    maxId = db.session.query(func.max(model.id)).scalar()
    return (maxId + 1) if maxId else 1