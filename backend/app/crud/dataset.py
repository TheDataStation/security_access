import os
from tempfile import SpooledTemporaryFile
from typing import List, Any, Optional
from uuid import uuid4

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.models import Dataset, File
from app.schemas import DatasetCreate, DatasetUpdate


class CRUDFile:
    def create(
        self, db: Session, *, sharer_id: int, filename: str, file: SpooledTemporaryFile
    ) -> File:
        fp = f"datasets_dir/{uuid4()}"
        open(fp, "wb").write(file.read())
        file_obj = File(url=fp, name=filename, sharer_id=sharer_id)
        db.add(file_obj)
        db.commit()
        db.refresh(file_obj)
        return file_obj

    def get(self, db: Session, id: int) -> File:
        return db.query(File).filter(File.id == id).first()

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

    def remove(self, db: Session, *, id: int) -> File:
        obj: File = db.query(File).get(id)
        db.delete(obj)
        os.remove(obj.url)
        db.commit()
        return obj



class CRUDDataset:
    def create(
        self, db: Session, *, obj_in: DatasetCreate, sharer_id: int
    ) -> Dataset:
        dataset_obj = Dataset(
            title=obj_in.title,
            description=obj_in.description,
            sharer_id=sharer_id,
        )
        db.add(dataset_obj)
        db.commit()
        db.refresh(dataset_obj)
        for file_id in obj_in.file_ids:
            file = db.query(File).filter(File.id == file_id).one()
            file.dataset_id = dataset_obj.id
            db.commit()

        return dataset_obj

    def get(self, db: Session, id: int) -> Dataset:
        return db.query(Dataset).filter(Dataset.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, sharer_id: int = None
    ) -> List[Dataset]:
        q = db.query(Dataset)
        if sharer_id is not None:
            q = q.filter(Dataset.sharer_id == sharer_id)

        return q.offset(skip).limit(limit).all()

    def update(self, db: Session, *, db_obj: Dataset, obj_in: DatasetUpdate) -> Dataset:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Dataset:
        obj = db.query(Dataset).get(id)
        db.delete(obj)
        db.commit()
        return obj
