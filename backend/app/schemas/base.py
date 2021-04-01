import datetime

from pydantic import BaseModel


class AllDBEntities(BaseModel):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True
