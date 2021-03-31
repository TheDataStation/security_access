from typing import Optional, List, Union

from pydantic import BaseModel, PrivateAttr

from app.schemas.base import AllDBEntities
from app.schemas.base64 import Base64Bytes


class Url(BaseModel):
    url: str
    _dataset_id: int = PrivateAttr()


class DatasetBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

# Properties to receive on dataset creation
class DatasetCreate(DatasetBase):
    title: str
    # data: List[Base64Bytes]
    data: List[str]


# Properties to receive on dataset update
class DatasetUpdate(DatasetBase):
    pass


# Properties shared by models stored in DB
class DatasetCreatedInDBBase(DatasetBase, AllDBEntities):
    url_ids: List[int]


# Properties to return to client
class Dataset(DatasetCreatedInDBBase):
    pass


# Properties stored in DB
class DatasetInDB(DatasetCreatedInDBBase):
    _sharer_id: int = PrivateAttr()
