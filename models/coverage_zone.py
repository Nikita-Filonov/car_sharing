from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from models.base import BaseModel


class CoverageZone(BaseModel):
    __tablename__ = 'coverage_zone'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), comment='Name', nullable=False)

    @classmethod
    def get_initial(cls, session: Session) -> 'CoverageZone':
        coverage_zone = cls.get(session, name='primary')

        if coverage_zone is None:
            return cls.create(session, name='primary')

        return coverage_zone
