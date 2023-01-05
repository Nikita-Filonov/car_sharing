from enum import Enum

from sqlalchemy import Column, Float, ForeignKey, Integer, String

from exceptions.users import NotAcceptableRating
from models.base import BaseModel
from settings import DEFAULT_RATING


class UserStatus(str, Enum):
    REVOKED = 'revoked'
    REGULAR = 'regular'
    INTERMEDIATE = 'intermediate'
    VIP = 'VIP'


class User(BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(200), nullable=False, comment='First name')
    last_name = Column(String(200), nullable=False, comment='Last name')
    middle_name = Column(String(200), nullable=False, comment='Middle name')
    rating = Column(Float, default=DEFAULT_RATING, comment='Rating')
    coverage_zone_id = Column(
        Integer, ForeignKey('coverage_zone.id', ondelete='CASCADE'), nullable=False
    )

    @property
    def status(self) -> UserStatus:
        if (self.rating >= 0) and (self.rating < 4):
            return UserStatus.REVOKED

        if (self.rating >= 4.0) and (self.rating < 4.5):
            return UserStatus.REGULAR

        if (self.rating >= 4.5) and (self.rating < 4.75):
            return UserStatus.INTERMEDIATE

        if (self.rating >= 4.75) and (self.rating <= 5):
            return UserStatus.VIP

        raise NotAcceptableRating(
            f'Not acceptable rating value "{self.rating}"'
        )
