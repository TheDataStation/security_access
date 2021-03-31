import datetime

from pydantic import BaseModel, PrivateAttr


class AllDBEntities(BaseModel):
    _id: int = PrivateAttr()
    created_at: datetime.datetime

    class Config:
        orm_mode = True
