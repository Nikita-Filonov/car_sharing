from database import session
from models import CoverageZone, Trip, User

db_session = session()

coverage_zone = CoverageZone.get_initial(db_session)
user_again = User.create(
    db_session,
    first_name='Ulyana (Again)',
    last_name='Smith',
    middle_name='Alone',
    coverage_zone_id=coverage_zone.id
)

trip_first = Trip.book(
    db_session,
    user_id=user_again.id,
    transport_id=1,
    coverage_zone_id=coverage_zone.id
)

trip_second = Trip.book(
    db_session,
    user_id=user_again.id,
    transport_id=1,
    coverage_zone_id=coverage_zone.id
)
