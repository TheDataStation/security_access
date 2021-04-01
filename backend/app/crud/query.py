from sqlalchemy.orm import Session

from app import schemas
from app.crud import access, access_grants_dataset
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
        with db.begin():
            accessdb = access.create(schemas.AccessCreate(), with_owner_id=sharer.id)
            access_grants_dataset.create(
                schemas.AccessGrantsDataset(
                    _access_id=accessdb.id, _dataset_id=dataset_id
                )
            )
            return super(CRUDQueryRequestsAccess, self).create(
                db, obj_in=obj_in, with_owner_id=accessdb.id
            )
