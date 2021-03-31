from typing import Type, Tuple, List, Union, Dict, Any, Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from app import schemas
from app.crud import CRUDBase
from app.db import models
from app.db.models import Dataset
from app.schemas import DatasetCreate, DatasetUpdate

url = CRUDBase[models.Url, schemas.Url, schemas.Url](
    models.Url, owner_attr="dataset_id"
)

DatasetAndUrlIDs = Tuple[Dataset, List[int]]


class CRUDDataset(CRUDBase[Dataset, DatasetCreate, DatasetUpdate]):
    def __init__(self, model: Dataset):
        super().__init__(model, owner_attr="sharer_id")

    # noinspection PyMethodOverriding
    def create(
        self, db: Session, *, obj_in: DatasetCreate, with_owner_id: int
    ) -> DatasetAndUrlIDs:
        # TODO(max): this breaks if user isn't a sharer
        dataset_obj = Dataset(
            title=obj_in.title,
            description=obj_in.description,
            sharer_id=with_owner_id,
        )
        db.add(dataset_obj)
        db.commit()
        db.refresh(dataset_obj)
        url_ids = []
        for datum in obj_in.data:
            fp = f"datasets_dir/{uuid4()}"
            open(fp, "w").write(datum)
            url_ids.append(
                url.create(
                    db, obj_in=schemas.Url(url=fp), with_owner_id=dataset_obj.id
                ).id
            )
        return dataset_obj, url_ids

    def get(self, db: Session, id: Any) -> DatasetAndUrlIDs:
        dataset = super().get(db, id)
        url_ids = [u.id for u in url.get_multi(db=db, with_owner_id=dataset.id)]
        return dataset, url_ids

    # noinspection PyMethodOverriding
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, with_owner_id: int = None
    ) -> List[DatasetAndUrlIDs]:
        datasets = super().get_multi(
            db, skip=skip, limit=limit, with_owner_id=with_owner_id
        )
        url_ids = [
            [u.id for u in url.get_multi(db=db, with_owner_id=dataset.id)]
            for dataset in datasets
        ]
        return list(zip(datasets, url_ids))

    def update(self, db: Session, *, db_obj, obj_in) -> DatasetAndUrlIDs:
        dataset = super().update(db, db_obj=db_obj, obj_in=obj_in)
        url_ids = [u.id for u in url.get_multi(db=db, with_owner_id=dataset.id)]
        return dataset, url_ids
