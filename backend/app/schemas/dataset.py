from typing import Optional, List

from pydantic import BaseModel

from app.schemas.base import AllDBEntities


class File(AllDBEntities):
    name: str
    sharer_id: int


class FileInDB(File):
    dataset_id: int
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
    sharer_id: int
