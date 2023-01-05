from database import session
from models import CoverageZone, Trip, User

db_session = session()

coverage_zone = CoverageZone.get_initial(db_session)
user_high = User.create(
    db_session,
    first_name='Ulyana (High)',
    last_name='Smith',
    middle_name='Alone',
    coverage_zone_id=coverage_zone.id
)

user_low = User.create(
    db_session,
    first_name='Ulyana (Low)',
    last_name='Smith',
    middle_name='Alone',
    coverage_zone_id=coverage_zone.id
)

trip_high = Trip.book(
    db_session,
    user_id=user_high.id,
    transport_id=1,
    coverage_zone_id=coverage_zone.id
)
trip_high.start(db_session)


trip_low = Trip.book(
    db_session,
    user_id=user_low.id,
    transport_id=1,
    coverage_zone_id=coverage_zone.id
)
trip_low.start(db_session)
