from datetime import datetime

import inflection
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    CheckConstraint,
    MetaData,
    PrimaryKeyConstraint,
)
from sqlalchemy.dialects.sqlite import JSON, BLOB

from sqlalchemy.ext.declarative import as_declarative, declared_attr

from app.db.session import engine

metadata = MetaData(bind=engine)


@as_declarative(metadata=metadata)
class Base:
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return inflection.underscore(cls.__name__.lower())


class AllEntities(object):
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now())


class User(Base, AllEntities):
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean(), default=False)
    full_name = Column(String, index=True)


class Querier(User):
    id = Column(Integer, ForeignKey("user.id"), primary_key=True, nullable=False)


class Sharer(User):
    id = Column(Integer, ForeignKey("user.id"), primary_key=True, nullable=False)


class Operator(User):
    id = Column(Integer, ForeignKey("user.id"), primary_key=True, nullable=False)


class Url(Base, AllEntities):
    url = Column(String, unique=True, index=True)
    dataset_id = Column(Integer, ForeignKey("dataset.id"), nullable=False)


class Dataset(Base, AllEntities):
    sharer_id = Column(Integer, ForeignKey("sharer.id"), nullable=False)


class Query(Base, AllEntities):
    querier_id = Column(Integer, ForeignKey("querier.id"), nullable=False)
    status = Column(
        String,
        CheckConstraint("status IN ('pending', 'started','succeeded','failed')"),
        default="pending",
        nullable=False,
    )
    type = Column(
        String,
        CheckConstraint("type IN ('dod','blindml','catalog', 'other')"),
        nullable=False,
    )
    payload = Column(JSON, nullable=False)

    input_data = Column(BLOB)
    status_reason = Column(String)
    description = Column(String)


# this is an association table
class QueryUsesDataset(Base):
    __table_args__ = (PrimaryKeyConstraint("query_id", "dataset_id"),)

    query_id = Column(Integer, ForeignKey("query.id"), nullable=False)
    dataset_id = Column(Integer, ForeignKey("dataset.id"), nullable=False)


class QueryRequestsAccess(Base):
    __table_args__ = (PrimaryKeyConstraint("query_id", "access_id"),)

    created_at = Column(DateTime, default=datetime.now())

    reveal_input_data = Column(Boolean, default=False)
    reveal_querier = Column(Boolean, default=False)
    query_id = Column(Integer, ForeignKey("query.id"), nullable=False)
    access_id = Column(Integer, ForeignKey("access.id"), nullable=False)

    expiry = Column(DateTime)


class Access(Base, AllEntities):
    __table_args__ = (
        CheckConstraint(
            # this is actually an if then (a | b) <=> if a then b
            "decision = 'maybe' OR (decision_reason IS NOT NULL AND length(decision_reason) > 0)"
        ),
    )

    sharer_id = Column(Integer, ForeignKey("sharer.id"), nullable=False)
    decision = Column(
        String,
        CheckConstraint("decision IN ('yes','no','maybe','pending')"),
        default="pending",
        nullable=False,
    )

    reveal_sharer = Column(Boolean, default=False)
    decision_reason = Column(String)
    expiry = Column(DateTime)


# this is an association table
class AccessGrantsDataset(Base):
    __table_args__ = (PrimaryKeyConstraint("access_id", "dataset_id"),)

    access_id = Column(Integer, ForeignKey("access.id"), nullable=False)
    dataset_id = Column(Integer, ForeignKey("dataset.id"), nullable=False)
