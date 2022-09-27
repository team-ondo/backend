from sqlalchemy import create_engine

from src.constants.common import SYNC_DATABASE_URL
from src.models import models

engine = create_engine(SYNC_DATABASE_URL, echo=True)


def drop_database() -> None:
    models.Base.metadata.drop_all(engine)


def create_database() -> None:
    models.Base.metadata.create_all(engine)


def reset_database() -> None:
    drop_database()
    create_database()


if __name__ == "__main__":
    reset_database()
