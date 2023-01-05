from database import session
from models import CoverageZone, Trip, User

db_session = session()

coverage_zone = CoverageZone.get_initial(db_session)
user = User.create(
    db_session,
    first_name='Ulyana (Does not have access to VIP)',
    last_name='Smith',
    middle_name='Alone',
    coverage_zone_id=coverage_zone.id
)

trip = Trip.book(
    db_session,
    user_id=user.id,
    transport_id=3,
    coverage_zone_id=coverage_zone.id
)
trip.start(db_session)
