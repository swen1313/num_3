from sqlmodel import Session, create_engine

from src.core import config, config_all

__all__ = ("get_session",)


engine = create_engine(config_all.DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
