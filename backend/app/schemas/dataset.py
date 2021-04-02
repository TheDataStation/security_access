from typing import Optional, List

from pydantic import BaseModel, PrivateAttr

from app.schemas.base import AllDBEntities


class File(AllDBEntities):
    name: str
    _sharer_id: int = PrivateAttr()


class FileInDB(File):
    _dataset_id: int = PrivateAttr()
    url: str


class DatasetBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on dataset creation
class DatasetCreate(DatasetBase):
    title: str
    file_ids: List[int]


# Properties to receive on dataset update
class DatasetUpdate(DatasetBase):
    pass


# Properties to return to client
class Dataset(DatasetCreate, AllDBEntities):
    pass


# Properties stored in DB
class DatasetInDB(DatasetCreate):
    _sharer_id: int = PrivateAttr()
