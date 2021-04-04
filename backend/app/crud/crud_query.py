from typing import List

from sqlalchemy.orm import Session

from app import schemas
from .crud_access import (
    access as crud_access,
    access_grants_dataset as crud_access_grants_dataset,
)
from .base import CRUDBase
from app.db import models

query = CRUDBase[models.Query, schemas.QueryCreate, schemas.QueryUpdate](
    models.Query, owner_attr="querier_id"
)


class CRUDQueryRequestsAccess(
    CRUDBase[
        models.QueryRequestsAccess,
        schemas.QueryRequestsAccess,
        schemas.QueryRequestsAccess,
    ]
):
    def __init__(self):
        super(CRUDQueryRequestsAccess, self).__init__(
            models.QueryRequestsAccess, owner_attr="access_id"
        )

    def create_query_requests_access_and_access(
        self, db: Session, *, query_id: int, dataset_id: int
    ) -> models.QueryRequestsAccess:
        (sharer_id,) = (
            db.query(models.Dataset.sharer_id)
            .where(models.Dataset.id == dataset_id)
            .one()
        )
        access_db = crud_access.create(
            db, obj_in=schemas.AccessCreate(), with_owner_id=sharer_id
        )
        crud_access_grants_dataset.create(
            db,
            obj_in=schemas.AccessGrantsDatasetBase(
                access_id=access_db.id, dataset_id=dataset_id
            ),
            with_owner_id=access_db.id,
        )
        return self.create(
            db,
            obj_in=schemas.QueryRequestsAccessCreate(
                query_id=query_id, access_id=access_db.id
            ),
            with_owner_id=query_id,
        )


query_requests_access = CRUDQueryRequestsAccess()
query_uses_dataset = CRUDBase[
    models.QueryUsesDataset, schemas.QueryUsesDataset, schemas.QueryUsesDataset
](models.QueryUsesDataset, owner_attr="query_id")


def get_query_for_query_request(db: Session, query_request_id: int) -> models.Query:
    join_query = (
        db.query(models.Query)
        .join(
            models.QueryRequestsAccess,
            models.Query.id == models.QueryRequestsAccess.query_id,
        )
        .filter(models.QueryRequestsAccess.id == query_request_id)
    )
    return join_query.one()


def get_queries_for_query_requests(
    db: Session, query_request_ids: List[int]
) -> List[models.Query]:
    join_query = (
        db.query(models.Query)
        .join(
            models.QueryRequestsAccess,
            models.Query.id == models.QueryRequestsAccess.query_id,
        )
        .filter(models.QueryRequestsAccess.id.in_(query_request_ids))
    )
    return join_query.all()
