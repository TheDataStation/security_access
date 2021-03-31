import datetime
from enum import auto
from typing import Optional, Union

from fastapi_utils.enums import StrEnum
from pydantic import BaseModel, Json, PrivateAttr

from app.schemas.base import AllDBEntities


class QueryStatus(StrEnum):
    pending = auto()
    started = auto()
    succeeded = auto()
    failed = auto()


class QueryType(StrEnum):
    dod = auto()
    blindml = auto()
    catalog = auto()
    other = auto()


class QueryBase(AllDBEntities):
    input_data: Optional[bytes] = None
    status: QueryStatus = QueryStatus.pending
    status_reason: Optional[str]
    type: Optional[QueryType]
    description: Optional[str]
    payload: Optional[Json]


# Properties to receive on query creation
class QueryCreate(QueryBase):
    status: QueryStatus = QueryStatus.pending
    type: QueryType
    payload: Json
    _querier_id: int = PrivateAttr()


class QueryUpdate(QueryBase):
    pass

class Query(QueryBase):
    pass


class QueryUsesDataset(BaseModel):
    _query_id: int = PrivateAttr()
    _dataset_id: int = PrivateAttr()


class QueryRequestsAccess(BaseModel):
    expiry: Optional[Union[datetime.datetime, datetime.timedelta]]
    reveal_input_data: Optional[bool] = None
    reveal_querier: Optional[bool] = None
    _query_id: int = PrivateAttr()
    _access_id: int = PrivateAttr()
