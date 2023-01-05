from typing import TypeVar

from sqlalchemy import select, update
from sqlalchemy.orm import Session, selectinload

from database import Base

T = TypeVar('T', bound='BaseModel')


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def get(cls: T, session: Session, load: list | tuple | None = None, **kwargs) -> T | None:
        query = select(cls).filter_by(**kwargs)

        if load:
            for table in load:
                query = query.options(selectinload(table))

        result = session.execute(query)
        return result.scalars().first()

    @classmethod
    def filter(
            cls: T,
            session: Session,
            select_values: list | tuple | None = None,
            order_by: list | tuple | None = None,
            slice_query: list | tuple | None = None,
            clause_filter: list | tuple | None = None,
            join: list | tuple | None = None,
            load: list | tuple | None = None,
            **kwargs
    ) -> list[T]:
        query = select(select_values or cls).filter_by(**kwargs)
        if order_by:
            query = query.order_by(*order_by)

        if slice_query:
            query = query.slice(*slice_query)

        if clause_filter:
            query = query.filter(*clause_filter)

        if load:
            for table in load:
                query = query.options(selectinload(table))

        if join:
            for join_table in join:
                query = query.join(join_table)

        result = session.execute(query)
        return result.scalars().all()

    @classmethod
    def create(cls: T, session: Session, **kwargs) -> T:
        model = cls(**kwargs)
        session.add(model)
        session.commit()
        session.flush(model)

        return model

    @classmethod
    def delete(cls: T, session: Session, **kwargs) -> None:
        model = cls.get(session, **kwargs)

        if model is None:
            raise NotImplementedError('Row is not found')

        session.delete(model)
        session.commit()

    def update(self: T, session: Session, **kwargs) -> T:
        query = update(self.__class__).filter_by(id=self.id).values(**kwargs)
        session.execute(query)
        session.commit()
        session.flush(self)

    @classmethod
    def exists(cls: T, session: Session, clause_filter: tuple = None, **kwargs) -> bool:
        query = select(cls.id).filter_by(**kwargs)

        if clause_filter:
            query = query.filter(*clause_filter)

        result = session.execute(query)
        return bool(result.first())
