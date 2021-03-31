from typing import Optional, List, Union

from pydantic import BaseModel, PrivateAttr

from app.schemas.base import AllDBEntities


class Url(BaseModel):
    url: str
    _dataset_id: int = PrivateAttr()


class DatasetBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    urls: Optional[List[Union[str, int]]] = None


# Properties to receive on dataset creation
class DatasetCreate(DatasetBase):
    title: str
    urls: List[str]


# Properties to receive on dataset update
class DatasetUpdate(DatasetBase):
    pass


# Properties shared by models stored in DB
class DatasetCreatedInDBBase(DatasetBase, AllDBEntities):
    pass


# Properties to return to client
class Dataset(DatasetCreatedInDBBase):
    pass


# Properties stored in DB
class DatasetInDB(DatasetCreatedInDBBase):
    _sharer_id: int = PrivateAttr()
    _url_ids: List[int] = PrivateAttr()
