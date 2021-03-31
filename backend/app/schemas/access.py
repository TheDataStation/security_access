import datetime
from enum import auto
from typing import Optional, Union

from fastapi_utils.enums import StrEnum
from pydantic import BaseModel, PrivateAttr



class AccessDecision(StrEnum):
    yes = auto()
    no = auto()
    maybe = auto()
    pending = auto()


class AccessBase(BaseModel):
    expiry: Optional[Union[datetime.datetime, datetime.timedelta]] = None
    reveal_sharer: Optional[bool] = None
    decision: Optional[AccessDecision] = None
    decision_reason: Optional[str] = None


# Properties to receive on access creation
class AccessCreate(AccessBase):
    decision: AccessDecision = AccessDecision.pending


# Properties to receive on access update
class AccessUpdate(AccessBase):
    pass


class Access(AccessBase):
    _sharer_id: int = PrivateAttr()


class AccessGrantsDataset(BaseModel):
    _access_id: int = PrivateAttr()
    _dataset_id: int = PrivateAttr()
