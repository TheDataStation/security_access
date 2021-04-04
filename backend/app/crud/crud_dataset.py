from tempfile import SpooledTemporaryFile
from typing import List, Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from app import schemas
from app.crud.base import CRUDBase
from app.db import models
from app.db.models import Dataset, File
from app.schemas import DatasetCreate


class CRUDFile(
    CRUDBase[
        models.File,
        schemas.File,
        schemas.File,
    ]
):
    def create(
        self,
        db: Session,
        *,
        with_owner_id: int,
        filename: str,
        file: SpooledTemporaryFile,
    ) -> File:
        fp = f"datasets_dir/{uuid4()}"
        open(fp, "wb").write(file.read())
        file_obj = File(url=fp, name=filename, sharer_id=with_owner_id)
        db.add(file_obj)
        db.commit()
        db.refresh(file_obj)
        return file_obj

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        dataset_id: Optional[int] = None,
        sharer_id: Optional[int] = None,
    ) -> List[File]:

        q = db.query(File)

        if sharer_id is not None:
            q = q.filter(File.sharer_id == sharer_id)
        if dataset_id is not None:
            q = q.filter(File.dataset_id == dataset_id)

        return q.offset(skip).limit(limit).all()


class CRUDDataset(
    CRUDBase[
        models.Dataset,
        schemas.DatasetCreate,
        schemas.DatasetUpdate,
    ]
):
    def create(
        self, db: Session, *, obj_in: DatasetCreate, with_owner_id: Optional[int] = None
    ) -> Dataset:
        dataset_obj = Dataset(
            title=obj_in.title,
            description=obj_in.description,
            sharer_id=with_owner_id,
        )
        db.add(dataset_obj)
        db.commit()
        db.refresh(dataset_obj)
        for file_id in obj_in.file_ids:
            file = db.query(File).filter(File.id == file_id).one()
            file.dataset_id = dataset_obj.id
            db.commit()

        return dataset_obj


dataset = CRUDDataset(models.Dataset, owner_attr="sharer_id")
file = CRUDFile(models.File, owner_attr="sharer_id")


def get_datasets_for_query(db: Session, query_id: int):
    join_query = (
        db.query(models.Dataset)
        .join(models.QueryUsesDataset)
        .filter(models.QueryUsesDataset.query_id == query_id)
    )
    return join_query.all()

def get_files_by_name(db: Session, name: str) -> List[models.File]:
    return db.query(models.File).filter(models.File.name == name).all()