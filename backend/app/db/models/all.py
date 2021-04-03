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
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.ext.declarative import declared_attr, declarative_base

from app.db.session import engine

metadata = MetaData(bind=engine)
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now())

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_operator = Column(Boolean(), default=False)
    full_name = Column(String, index=True)


class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now())

    url = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    dataset_id = Column(Integer, ForeignKey("dataset.id"))
    sharer_id = Column(Integer, ForeignKey("user.id"), nullable=False)


class Dataset(Base):
    __tablename__ = 'dataset'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now())

    title = Column(String, index=True)
    description = Column(String, index=True)
    sharer_id = Column(Integer, ForeignKey("user.id"), nullable=False)


class Query(Base):
    __tablename__ = 'query'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now())

    querier_id = Column(Integer, ForeignKey("user.id"), nullable=False)
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

    status_reason = Column(String)
    description = Column(String)


# this is an association table
class QueryUsesDataset(Base):
    __tablename__ = 'query_uses_dataset'
    __table_args__ = (PrimaryKeyConstraint("query_id", "dataset_id"),)

    query_id = Column(Integer, ForeignKey("query.id"), nullable=False)
    dataset_id = Column(Integer, ForeignKey("dataset.id"), nullable=False)


class QueryRequestsAccess(Base):
    __tablename__ = 'query_requests_access'
    __table_args__ = (PrimaryKeyConstraint("query_id", "access_id"),)

    created_at = Column(DateTime, default=datetime.now())

    reveal_input_data = Column(Boolean, default=False)
    reveal_querier = Column(Boolean, default=False)
    query_id = Column(Integer, ForeignKey("query.id"), nullable=False)
    access_id = Column(Integer, ForeignKey("access.id"), nullable=False)

    expiry = Column(DateTime)


class Access(Base):
    __tablename__ = 'access'
    __table_args__ = (
        CheckConstraint(
            # this is actually an if then (a | b) <=> if a then b
            "decision = 'maybe' OR (decision_reason IS NOT NULL AND length(decision_reason) > 0)"
        ),
    )
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now())

    sharer_id = Column(Integer, ForeignKey("user.id"), nullable=False)
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
    __tablename__ = 'access_grants_dataset'
    __table_args__ = (PrimaryKeyConstraint("access_id", "dataset_id"),)

    access_id = Column(Integer, ForeignKey("access.id"), nullable=False)
    dataset_id = Column(Integer, ForeignKey("dataset.id"), nullable=False)
