import datetime
from enum import auto
from typing import Optional, Union

from fastapi_utils.enums import StrEnum
from pydantic import BaseModel, Json

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
class QueryCreate(BaseModel):
    type: QueryType
    description: Optional[str]
    payload: Json


class QueryUpdate(QueryBase):
    pass


class Query(QueryBase):
    querier_id: int


class QueryUsesDataset(BaseModel):
    query_id: int
    dataset_id: int


class QueryRequestsAccess(AllDBEntities):
    expiry: Optional[Union[datetime.datetime, datetime.date, datetime.timedelta]]

    reveal_input_data: Optional[bool] = None
    reveal_querier: Optional[bool] = None
    query_id: int
    access_id: int

class QueryRequestsAccessCreate(BaseModel):
    query_id: int
    access_id: int

class QueryRequestsAccessUpdate(BaseModel):
    expiry: Optional[Union[datetime.datetime, datetime.date, datetime.timedelta]]
    reveal_input_data: Optional[bool] = None
    reveal_querier: Optional[bool] = None

