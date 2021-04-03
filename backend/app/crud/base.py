from typing import Dict, Generic, List, Optional, Type, TypeVar, Union, Any

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.models.all import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], owner_attr: Optional[str] = None):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        if owner_attr is not None:
            assert hasattr(
                model, owner_attr
            ), f"model {model.__name__} does not have attr {owner_attr}"

        self.owner_attr = owner_attr

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
            self,
            db: Session,
            *,
            skip: int = 0,
            limit: int = 100,
            with_owner_id: Optional[int] = None,
    ) -> List[ModelType]:

        q = db.query(self.model)
        if with_owner_id is not None:
            assert (
                    self.owner_attr is not None
            ), f"model {self.model.__name__} does not have owner attr"

            q = q.filter_by(**{self.owner_attr: with_owner_id})

        return q.offset(skip).limit(limit).all()

    def create(
            self,
            db: Session,
            *,
            obj_in: CreateSchemaType,
            with_owner_id: Optional[int] = None,
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)

        if with_owner_id is not None:
            assert (
                    self.owner_attr is not None
            ), f"model {self.model.__name__} does not have owner attr"
            obj_in_data[self.owner_attr] = with_owner_id
        if self.owner_attr is not None and with_owner_id is None:
            raise Exception(f"model {self.model.__name__} did not get with_owner_id")

        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
