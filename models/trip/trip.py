from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Session

from exceptions.trips import (ForbiddenToBookTransport,
                              TransportAlreadyReserved, TripAlreadyStarted,
                              UnknownTripPriceType)
from models.base import BaseModel
from models.transport.transport import Transport
from models.transport.transport_level import TransportLevel
from models.trip.trip_ride import TripRide, TripRideType
from models.user import User, UserStatus


class TripState(IntEnum):
    BOOKED = 1
    STARTED = 2
    FINISHED = 3


class TripPaymentType(IntEnum):
    PER_MINUTE = 1
    PER_HOUR = 2


@dataclass
class TripFinishResult:
    price: float
    total_ride_minutes: float
    total_await_minutes: float


class Trip(BaseModel):
    __tablename__ = 'trip'

    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_type = Column(
        Integer, default=TripPaymentType.PER_MINUTE, comment='Payment type'
    )
    transport_id = Column(
        Integer, ForeignKey('transport.id', ondelete='CASCADE'), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False
    )
    coverage_zone_id = Column(
        Integer, ForeignKey('coverage_zone.id', ondelete='CASCADE'), nullable=False
    )
    state = Column(Integer, nullable=False, comment='State')
    booked_at = Column(
        DateTime, comment='When the trip started', nullable=True
    )
    started_at = Column(
        DateTime, comment='When the trip started', nullable=True
    )
    finished_at = Column(
        DateTime, comment='When the trip finished', nullable=True
    )

    @classmethod
    def is_user_trip_started(cls, session: Session, user_id: int) -> bool:
        return cls.exists(
            session,
            clause_filter=(
                Trip.user_id == user_id,
                Trip.state.is_not(TripState.FINISHED),
            )
        )

    @classmethod
    def is_transport_reserved(cls, session: Session, transport_id: int) -> bool:
        return cls.exists(
            session,
            clause_filter=(
                Trip.transport_id == transport_id,
                Trip.state.is_not(TripState.FINISHED),
            )
        )

    @classmethod
    def is_user_allowed_to_book_transport(
        cls, session: Session, user_id: int, transport_id: int
    ) -> bool:
        user = User.get(session, id=user_id)

        if user.status == UserStatus.REVOKED:
            return False

        if user.status == UserStatus.VIP:
            return True

        transport = Transport.get(
            session, id=transport_id, load=(Transport.transport_level,)
        )

        return not (user.rating < transport.transport_level.min_rating)

    def get_trip_price(
        self, session: Session, total_ride_minutes: float, total_await_minutes: float
    ) -> float:
        transport = Transport.get(
            session, id=self.transport_id, load=(Transport.transport_level,)
        )
        level: TransportLevel = transport.transport_level

        if self.payment_type == TripPaymentType.PER_MINUTE:
            ride_price = total_ride_minutes * level.ride_price_per_minute
            await_price = total_await_minutes * level.await_price_per_minute
            return ride_price + await_price

        if self.payment_type == TripPaymentType.PER_HOUR:
            ride_price = (total_ride_minutes / 60) * level.ride_price_per_hour
            await_price = (total_await_minutes / 60) * \
                level.await_price_per_hour
            return ride_price + await_price

        raise UnknownTripPriceType(
            f'Unknown trip payment type "{self.payment_type}"'
        )

    @classmethod
    def book(cls, session: Session, user_id: int, transport_id: int, coverage_zone_id: int):
        if cls.is_user_trip_started(session, user_id):
            raise TripAlreadyStarted(
                f'Trip for user with id "{user_id}" already exists'
            )

        if cls.is_transport_reserved(session, transport_id):
            raise TransportAlreadyReserved(
                f'Transport with id "{transport_id}" already in use'
            )

        if not cls.is_user_allowed_to_book_transport(session, user_id, transport_id):
            raise ForbiddenToBookTransport(
                f'User with id "{user_id}" not able to book transport with id "{transport_id}"'
            )

        return cls.create(
            session,
            state=TripState.BOOKED,
            user_id=user_id,
            transport_id=transport_id,
            coverage_zone_id=coverage_zone_id,
            booked_at=datetime.now()
        )

    def start(self, session: Session):
        self.update(
            session, state=TripState.STARTED, started_at=datetime.now()
        )

    def finish(self, session: Session, user_id: int) -> TripFinishResult:
        self.update(
            session, state=TripState.FINISHED, finished_at=datetime.now()
        )

        user_rating = TripRide.get_user_rating(session, trip_id=self.id)
        user = User.get(session, id=user_id)
        user.update(session, rating=user.rating + user_rating)

        total_ride_minutes = TripRide.get_total_minutes(
            session, trip_id=self.id, ride_type=TripRideType.RIDE
        )
        total_await_minutes = TripRide.get_total_minutes(
            session, trip_id=self.id, ride_type=TripRideType.AWAIT
        )
        price = self.get_trip_price(
            session, total_ride_minutes, total_await_minutes
        )

        return TripFinishResult(
            price=price,
            total_ride_minutes=total_ride_minutes,
            total_await_minutes=total_await_minutes
        )
