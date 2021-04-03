import json
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.crud import get_accesses_for_queries
from app.db import models

router = APIRouter()


@router.get("/", response_model=List[schemas.Query])
def read_queries(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve querys.
    """
    if crud.user.is_operator(current_user):
        queries = crud.query.get_multi(db, skip=skip, limit=limit)
    else:
        queries = crud.query.get_multi(
            db=db, with_owner_id=current_user.id, skip=skip, limit=limit
        )
    for q in queries:
        q.payload = json.dumps(q.payload)
    return queries


# in case query includes data (then it will be stored as a dataset)
class DatasetID(BaseModel):
    dataset_id: Optional[int]


@router.post("/", response_model=schemas.Query)
def create_query(
    *,
    db: Session = Depends(deps.get_db),
    query_in: schemas.QueryCreate,
    dataset_id: DatasetID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new query.
    """
    dataset_id = dataset_id.dataset_id
    query = crud.query.create(db=db, obj_in=query_in, with_owner_id=current_user.id)
    if dataset_id is not None:
        crud.query_uses_dataset.create(
            db,
            obj_in=schemas.QueryUsesDataset(dataset_id=dataset_id, query_id=query.id),
            with_owner_id=query.id
        )
        access = crud.access.create(
            db,
            obj_in=schemas.AccessCreate(
                decision=schemas.AccessDecision.yes,
                decision_reason="submitted with query",
            ),
            with_owner_id=current_user.id,
        )
        crud.access_grants_dataset.create(
            db,
            obj_in=schemas.AccessGrantsDataset(access_id=access.id, dataset_id=dataset_id),
            with_owner_id = access.id
        )
    query.payload = json.dumps(query.payload)
    return query


@router.put("/{id}", response_model=schemas.Query)
def update_query(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    query_in: schemas.QueryUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an query.
    """
    query = crud.query.get(db=db, id=id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    if not crud.user.is_operator(current_user) and (
        query.querier_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    query = crud.query.update(db=db, db_obj=query, obj_in=query_in)
    return query


@router.get("/{id}", response_model=schemas.Query)
def read_query(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get query by ID.
    """
    query = crud.query.get(db=db, id=id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    if not crud.user.is_operator(current_user) and (
        query.querier_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return query


@router.delete("/{id}", response_model=schemas.Query)
def delete_query(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an query.
    """
    query = crud.query.get(db=db, id=id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    if not crud.user.is_operator(current_user) and (
        query.querier_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    query = crud.query.remove(db=db, id=id)
    return query


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
    """
    Retrieve accessGrantsDatasetes.
    """
    access_receipts = []
    if crud.user.is_operator(current_user):
        sharer_access_grants = crud.access.get_multi(db, skip=skip, limit=limit)
    else:
        sharer_access_grants = crud.access.get_multi(db, skip=skip, limit=limit, with_owner_id=current_user.id)
        queries = crud.query.get_multi(
            db=db, with_owner_id=current_user.id, skip=skip, limit=limit
        )

        # query -> query requests access -> access
        access_receipts = get_accesses_for_queries(db, [q.id for q in queries])

    return BothAccess(
        access_grants=sharer_access_grants,
        access_receipts=access_receipts,
    )
