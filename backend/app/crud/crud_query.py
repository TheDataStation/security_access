from typing import List

from sqlalchemy.orm import Session

from app import schemas
from app.crud.base import CRUDBase
from app.db import models


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

    # noinspection PyMethodOverriding
    def create(
            self, db: Session, *, obj_in: schemas.QueryRequestsAccess, dataset_id: int
    ) -> models.QueryRequestsAccess:
        sharer = (
            db.query(models.Dataset.sharer_id)
                .where(models.Dataset.id == dataset_id)
                .one()
        )
        access_db = access.create(schemas.AccessCreate(), with_owner_id=sharer.id)
        access_grants_dataset.create(
            db,
            obj_in=schemas.AccessGrantsDataset(
                access_id=access_db.id, dataset_id=dataset_id
            ),
            with_owner_id=access_db.id
        )
        return super(CRUDQueryRequestsAccess, self).create(
            db, obj_in=obj_in, with_owner_id=access_db.id
        )


query = CRUDBase[models.Query, schemas.QueryCreate, schemas.QueryUpdate](
    models.Query, owner_attr="querier_id"
)
query_requests_access = CRUDQueryRequestsAccess()
query_uses_dataset = CRUDBase[models.QueryUsesDataset, schemas.QueryUsesDataset, schemas.QueryUsesDataset](
    models.QueryUsesDataset, owner_attr="query_id"
)

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
