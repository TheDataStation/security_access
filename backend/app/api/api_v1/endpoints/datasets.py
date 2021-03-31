from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.crud
import app.crud.dataset
from app import crud, schemas
from app.db import models
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Dataset])
def read_datasets(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve datasets.
    """
    if crud.user.is_superuser(current_user):
        datasets = app.crud.dataset.get_multi(db, skip=skip, limit=limit)
    else:
        datasets = app.crud.dataset.get_multi(
            db=db, with_owner_id=current_user.id, skip=skip, limit=limit
        )
    return datasets


@router.post("/", response_model=schemas.Dataset)
def create_dataset(
    *,
    db: Session = Depends(deps.get_db),
    dataset_in: schemas.DatasetCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new dataset.
    """
    dataset = app.crud.dataset.create(db=db, obj_in=dataset_in, with_owner_id=current_user.id)
    return dataset


@router.put("/{id}", response_model=schemas.Dataset)
def update_dataset(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    dataset_in: schemas.DatasetUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an dataset.
    """
    dataset = app.crud.dataset.get(db=db, id=id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if not crud.user.is_superuser(current_user) and (dataset.sharer_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    dataset = app.crud.dataset.update(db=db, db_obj=dataset, obj_in=dataset_in)
    return dataset


@router.get("/{id}", response_model=schemas.Dataset)
def read_dataset(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get dataset by ID.
    """
    dataset = app.crud.dataset.get(db=db, id=id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if not crud.user.is_superuser(current_user) and (dataset.sharer_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return dataset


@router.delete("/{id}", response_model=schemas.Dataset)
def delete_dataset(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an dataset.
    """
    dataset = app.crud.dataset.get(db=db, id=id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if not crud.user.is_superuser(current_user) and (dataset.sharer_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    dataset = app.crud.dataset.remove(db=db, id=id)
    return dataset
