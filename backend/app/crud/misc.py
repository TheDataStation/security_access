from sqlalchemy.orm import Session

from app.db import models


def get_accesses_for_query(db: Session, query_id: int):
    join_query = (
        db.query(models.Access)
        .join(models.QueryRequestsAccess)
        .filter(models.QueryRequestsAccess.query_id == query_id)
    )
    return join_query.all()


def get_accesses_for_sharer(db: Session, sharer_id: int):
    join_query = (
        db.query(models.Access)
        .join(models.QueryRequestsAccess)
        .filter(models.Access.sharer_id == sharer_id)
    )
    return join_query.all()


def get_datasets_for_query(db: Session, query_id: int):
    join_query = (
        db.query(models.Dataset)
        .join(models.QueryUsesDataset)
        .filter(models.QueryUsesDataset.query_id == query_id)
    )
    return join_query.all()
