from sqlalchemy import Column, Float, Integer, String

from models.base import BaseModel


class TransportLevel(BaseModel):
    __tablename__ = 'transport_level'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment='Name')
    min_rating = Column(Float, nullable=False, comment='Min rating')
    ride_price_per_hour = Column(
        Float, nullable=False, comment='Ride price per hour'
    )
    await_price_per_hour = Column(
        Float, nullable=False, comment='Await price per hour'
    )
    ride_price_per_minute = Column(
        Float, nullable=False, comment='Ride price per minute'
    )
    await_price_per_minute = Column(
        Float, nullable=False, comment='Await price per minute'
    )
