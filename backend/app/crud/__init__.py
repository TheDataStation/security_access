from app import schemas
from app.db import models
from .base import CRUDBase
from .user import CRUDUser
from .dataset import CRUDDataset, url
from ..db.models import Dataset

access = CRUDBase[models.Access, schemas.AccessCreate, schemas.AccessUpdate](
    models.Access, owner_attr="sharer_id"
)
access_grants_dataset = CRUDBase[
    models.AccessGrantsDataset,
    schemas.AccessGrantsDataset,
    schemas.AccessGrantsDataset,
](models.AccessGrantsDataset)

user = CRUDUser(models.User)
# querier, sharer, operator

query = CRUDBase[models.Query, schemas.QueryCreate, schemas.QueryUpdate](
    models.Query, owner_attr="querier_id"
)
query_uses_dataset = CRUDBase[
    models.QueryUsesDataset,
    schemas.QueryUsesDataset,
    schemas.QueryUsesDataset,
](models.QueryUsesDataset)
dataset = CRUDDataset(Dataset)