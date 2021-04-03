from sqlalchemy.orm import Session

import app.crud.crud_user
from app import crud, schemas
from app.config import settings

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.db.models import all  # noqa: F401
from app.db.session import SessionLocal


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = app.crud.user.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            # this doesn't work for some reason?
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_active=True,
            is_superuser=True,
        )
        user = app.crud.user.user.create(db, obj_in=user_in)
        print(user)
    else:
        print("user already created")


def init() -> None:
    db = SessionLocal()
    init_db(db)


# do not run this from this directory
# run it from ../backend $ python -m app.db.init_db
if __name__ == "__main__":
    init()
