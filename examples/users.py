from database import session
from models import CoverageZone, User, Trip

db_session = session()

coverage_zone = CoverageZone.get_initial(db_session)
user = User.create(
    db_session,
    first_name='Ulyana',
    last_name='Smith',
    middle_name='Alone',
    coverage_zone_id=coverage_zone.id
)


print(f'{user.first_name=}, {user.status=}, {user.rating=}')

for rating in [3, 4.2, 4.6, 4.8]:
    user.update(db_session, rating=rating)
    print(f'{user.first_name=}, {user.status=}, {user.rating=}')


is_user_trip_started = Trip.is_user_trip_started(db_session, user.id)
print(f'{is_user_trip_started=}')
