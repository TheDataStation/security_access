from typing import List

from sqlalchemy.orm import Session

from app import schemas
from app.crud.base import CRUDBase
from app.db import models

access = CRUDBase[models.Access, schemas.AccessCreate, schemas.AccessUpdate](
    models.Access, owner_attr="sharer_id"
)
access_grants_dataset = CRUDBase[
    models.AccessGrantsDataset,
    schemas.AccessGrantsDataset,
    schemas.AccessGrantsDataset,
](models.AccessGrantsDataset, owner_attr="access_id")


def get_accesses_for_query(db: Session, query_id: int):
    join_query = (
        db.query(models.Access)
            .join(models.QueryRequestsAccess)
            .filter(models.QueryRequestsAccess.query_id == query_id)
    )
    return join_query.all()


def get_accesses_for_queries(db: Session, query_ids: List[int]):
    join_query = (
        db.query(models.Access)
            .join(models.QueryRequestsAccess)
            .filter(models.QueryRequestsAccess.query_id.in_(query_ids))
    )
    return join_query.all()