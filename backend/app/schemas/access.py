import datetime
from enum import auto
from typing import Optional, Union

from fastapi_utils.enums import StrEnum
from pydantic import BaseModel

from app.schemas.base import AllDBEntities


class AccessDecision(StrEnum):
    yes = auto()
    no = auto()
    maybe = auto()
    pending = auto()


class AccessBase(BaseModel):
    expiry: Optional[Union[datetime.datetime, datetime.date, datetime.timedelta]] = None
    reveal_sharer: Optional[bool] = None
    decision: Optional[AccessDecision] = None
    decision_reason: Optional[str] = None


# Properties to receive on access creation
class AccessCreate(AccessBase):
    decision: AccessDecision = AccessDecision.pending


# Properties to receive on access update
class AccessUpdate(AccessBase):
    pass


class AccessInDB(AccessBase, AllDBEntities):
    sharer_id: int

class Access(AccessBase, AllDBEntities):
    pass


class AccessGrantsDatasetBase(BaseModel):
    access_id: int
    dataset_id: int

class AccessGrantsDataset(AccessGrantsDatasetBase, AllDBEntities):
    pass
