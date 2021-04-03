import json
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.crud.crud_dataset import get_files_by_name
from app.crud.crud_query import (
    get_queries_for_query_requests,
    get_query_for_query_request,
)
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


# TODO(max): factor this factor (query requests access flow)
@router.post("/", response_model=schemas.Query)
def create_query(
    *,
    db: Session = Depends(deps.get_db),
    query_in: schemas.QueryCreate,
    dataset_id: DatasetID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> schemas.Query:
    """
    Create new query.
    """
    dataset_id = dataset_id.dataset_id
    query = crud.query.create(db=db, obj_in=query_in, with_owner_id=current_user.id)
    if dataset_id is not None:
        # TODO in particular this block
        crud.query_uses_dataset.create(
            db,
            obj_in=schemas.QueryUsesDataset(dataset_id=dataset_id, query_id=query.id),
            with_owner_id=query.id,
        )
        included_access = crud.access.create(
            db,
            obj_in=schemas.AccessCreate(
                decision=schemas.AccessDecision.yes,
                decision_reason="submitted with query",
            ),
            with_owner_id=current_user.id,
        )
        crud.access_grants_dataset.create(
            db,
            obj_in=schemas.AccessGrantsDatasetBase(
                access_id=included_access.id, dataset_id=dataset_id
            ),
            with_owner_id=included_access.id,
        )

        # TODO(max): hack to go through the access request flow
        files = crud.file.get_multi(db, dataset_id=dataset_id)
        if any(f.name == "Perovskite_Stability_with_features.csv" for f in files):
            extra_perovskite_file = get_files_by_name(
                db, "extra_Perovskite_Stability_with_features.csv"
            )
            assert len(extra_perovskite_file), "didn't upload extra perovskite file"
            extra_perovskite_ds = crud.dataset.get(db, extra_perovskite_file[0].dataset_id)
            crud.query_uses_dataset.create(
                db,
                obj_in=schemas.QueryUsesDataset(
                    dataset_id=extra_perovskite_ds.id, query_id=query.id
                ),
                with_owner_id=query.id,
            )
            crud.query_requests_access.create_query_requests_access_and_access(
                db,
                query_id=query.id,
                dataset_id=extra_perovskite_ds.id
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


@router.get("/{id}/requests_access", response_model=List[schemas.QueryRequestsAccess])
def read_query_requests_access_for_query(
    db: Session = Depends(deps.get_db),
    *,
    id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    if crud.user.is_operator(current_user):
        query_requests_access = crud.query_requests_access.get_multi(
            db=db, with_owner_id=id, skip=skip, limit=limit
        )
    else:
        query_requests_access = crud.query_requests_access.get_multi(
            db=db, with_owner_id=id, skip=skip, limit=limit
        )
        query_request_ids = [q.id for q in query_requests_access]
        for query in get_queries_for_query_requests(db, query_request_ids):
            if not query.querier_id != current_user.id:
                raise HTTPException(
                    status_code=400, detail="The user doesn't have enough privileges"
                )
    return query_requests_access


@router.get("/requests_access", response_model=List[schemas.QueryRequestsAccess])
def read_all_query_requests_access(
    db: Session = Depends(deps.get_db),
    *,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    query_requests_access = crud.query_requests_access.get_multi(
        db=db, skip=skip, limit=limit
    )
    if crud.user.is_operator(current_user):
        return query_requests_access
    else:
        query_request_ids = [q.id for q in query_requests_access]
        for query in get_queries_for_query_requests(db, query_request_ids):
            if not query.querier_id != current_user.id:
                raise HTTPException(
                    status_code=400, detail="The user doesn't have enough privileges"
                )
    return query_requests_access


@router.get("/requests_access/{id}", response_model=schemas.QueryRequestsAccess)
def update_query_requests_access(
    db: Session = Depends(deps.get_db),
    *,
    id: int,
    query_requests_access_in: schemas.QueryRequestsAccessUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    query_requests_access = crud.query_requests_access.get(db=db, id=id)
    if not query_requests_access:
        raise HTTPException(status_code=404, detail="Query request not found")

    query = get_query_for_query_request(db, query_requests_access.id)

    if not crud.user.is_operator(current_user) and (
        query.querier_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    query_requests_access = crud.query_requests_access.update(
        db=db, db_obj=query_requests_access, obj_in=query_requests_access_in
    )
    return query_requests_access
