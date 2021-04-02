import json
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
import app.crud
from app import crud, schemas
from app.api import deps
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
        queries = app.crud.query.get_multi(db, skip=skip, limit=limit)
    else:
        queries = app.crud.query.get_multi(
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
    query = app.crud.query.create(
        db=db, obj_in=query_in, with_owner_id=current_user.id
    )
    if dataset_id is not None:
        app.crud.query_uses_dataset.create(db, obj_in=schemas.QueryUsesDataset(
            dataset_id=dataset_id,
            query_id=query.id
        ))
        # TODO(max): immediate grant
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
    query = app.crud.query.get(db=db, id=id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    if not crud.user.is_operator(current_user) and (
            query.with_owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    query = app.crud.query.update(db=db, db_obj=query, obj_in=query_in)
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
    query = app.crud.query.get(db=db, id=id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    if not crud.user.is_operator(current_user) and (
            query.with_owner_id != current_user.id
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
    query = app.crud.query.get(db=db, id=id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    if not crud.user.is_operator(current_user) and (
            query.with_owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    query = app.crud.query.remove(db=db, id=id)
    return query
