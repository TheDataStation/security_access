from typing import Optional, List, Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

import app.crud.crud_access
from app import schemas, crud
from app.api import deps
from app.crud import get_accesses_for_queries
from app.db import models

access_router = APIRouter()


class BothAccess(BaseModel):
    access_grants: Optional[List[schemas.Access]]
    access_receipts: Optional[List[schemas.Access]]


@access_router.get("/", response_model=BothAccess)
def read_access_grants(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    access_receipts = []
    if crud.user.is_operator(current_user):
        sharer_access_grants = app.crud.crud_access.access.get_multi(db, skip=skip, limit=limit)
    else:
        sharer_access_grants = app.crud.crud_access.access.get_multi(db, skip=skip, limit=limit,
                                                                     with_owner_id=current_user.id)
        queries = crud.query.get_multi(
            db=db, with_owner_id=current_user.id, skip=skip, limit=limit
        )

        # query -> query requests access -> access
        access_receipts = get_accesses_for_queries(db, [q.id for q in queries])

    return BothAccess(
        access_grants=sharer_access_grants,
        access_receipts=access_receipts,
    )


@access_router.put("/{id}", response_model=schemas.Access)
def update_access(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        access_in: schemas.AccessUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an query.
    """
    access = crud.access.get(db=db, id=id)
    if not access:
        raise HTTPException(status_code=404, detail="Access not found")
    if not crud.user.is_operator(current_user) and (
            access.sharer_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    access = crud.access.update(db=db, db_obj=access, obj_in=access_in)
    return access
