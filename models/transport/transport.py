from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship

from models.base import BaseModel
from models.transport.transport_level import TransportLevel


class Transport(BaseModel):
    __tablename__ = 'transport'

    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String(200), nullable=False, comment='Brand')
    model = Column(String(200), nullable=False, comment='Model')
    max_speed = Column(Float, nullable=False, comment='Max speed')
    transport_level_id = Column(
        Integer, ForeignKey('transport_level.id', ondelete='CASCADE'), nullable=False
    )
    transport_level = relationship('TransportLevel')
    coverage_zone_id = Column(
        Integer, ForeignKey('coverage_zone.id', ondelete='CASCADE'), nullable=False
    )

    @classmethod
    def query(
        cls,
        session: Session,
        level: str | None = None,
        model: str | None = None
    ) -> list['Transport']:
        join = ()
        clause_filter = ()

        if level is not None:
            join += (TransportLevel,)
            clause_filter += (TransportLevel.name == level,)

        if model is not None:
            clause_filter += (cls.model == model,)

        return cls.filter(session, join=join, clause_filter=clause_filter)
