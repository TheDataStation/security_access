from typing import Type
from uuid import uuid4

from sqlalchemy.orm import Session

from app import schemas
from app.crud import CRUDBase
from app.crud.base import ModelType
from app.db import models
from app.db.models import Dataset
from app.schemas import DatasetCreate, DatasetUpdate

url = CRUDBase[models.Url, schemas.Url, schemas.Url](
    models.Url, owner_attr="dataset_id"
)

class CRUDDataset(CRUDBase[Dataset, DatasetCreate, DatasetUpdate]):
    def __init__(self, model: Type[ModelType]):
        super().__init__(model, owner_attr="sharer_id")

    # noinspection PyMethodOverriding
    def create(self, db: Session, *, obj_in: DatasetCreate, with_owner_id: int) -> Dataset:
        db_obj = Dataset(
            title=obj_in.title,
            description=obj_in.description,
            sharer_id=with_owner_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        for datum in obj_in.data:
            fp = f"datasets_dir/{uuid4()}"
            open(fp, "wb").write(datum)
            url.create(
                schemas.Url(
                   url=fp, _dataset_id=db_obj.id
                )
            )
        return db_obj

