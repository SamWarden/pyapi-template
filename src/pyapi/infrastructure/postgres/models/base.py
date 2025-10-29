import datetime

from sqlalchemy import MetaData, sql
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry

convention = {
    "ix": "ix_%(column_0_label)s",  # INDEX
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",  # UNIQUE
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # CHECK
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",  # FOREIGN KEY
    "pk": "pk_%(table_name)s",  # PRIMARY KEY
}

mapper_registry = registry(metadata=MetaData(naming_convention=convention))


class BaseModel(DeclarativeBase):
    registry = mapper_registry
    metadata = mapper_registry.metadata


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=sql.func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=sql.func.now(), onupdate=sql.func.now())
