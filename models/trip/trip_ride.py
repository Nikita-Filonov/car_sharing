from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Session

from models.base import BaseModel
from settings import MAX_SPEED, SUCCESS_RATING_INCREASE


class TripRideType(str, Enum):
    RIDE = 'ride'
    AWAIT = 'await'


class TripRide(BaseModel):
    __tablename__ = 'trip_ride'

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(
        Integer, ForeignKey('trip.id', ondelete='CASCADE'), nullable=False
    )
    ride_type = Column(String(20), comment='Trip ride type', nullable=False)
    initial_speed = Column(Float, comment='Initial speed', nullable=True)
    started_at = Column(DateTime, comment='Started at', nullable=False)
    finished_at = Column(DateTime, comment='Finished at', nullable=True)

    @classmethod
    def start(
        cls,
        session: Session,
        trip_id: int,
        ride_type: TripRideType,
        initial_speed: float | None = None
    ) -> 'TripRide':
        return cls.create(
            session,
            ride_type=ride_type,
            trip_id=trip_id,
            initial_speed=initial_speed,
            started_at=datetime.now()
        )

    def finish(self, session: Session) -> None:
        self.update(session, finished_at=datetime.now())

    @classmethod
    def get_total_minutes(cls, session: Session, trip_id: int, ride_type: TripRideType) -> float:
        trip_rides = cls.filter(session, trip_id=trip_id, ride_type=ride_type)
        return sum([
            (trip_ride.finished_at - trip_ride.started_at).seconds / 60
            for trip_ride in trip_rides
        ])

    @classmethod
    def get_user_rating(cls, session: Session, trip_id: int) -> float:
        trip_rides = cls.filter(
            session,
            trip_id=trip_id,
            clause_filter=(
                cls.initial_speed.is_not(None),
                cls.initial_speed > MAX_SPEED
            )
        )

        if not trip_rides:
            return SUCCESS_RATING_INCREASE

        penalty_ratings: list[float] = []

        for ride in trip_rides:
            minutes_delta = (ride.finished_at - ride.started_at).seconds / 60
            penalty_rating = ((ride.initial_speed - 60) / 120) * minutes_delta
            penalty_ratings.append(penalty_rating)

        return -round(sum(penalty_ratings), 2)
