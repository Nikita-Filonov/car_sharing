from time import sleep

from database import session
from models import CoverageZone, Trip, TripRide, User
from models.trip.trip import TripFinishResult
from models.trip.trip_ride import TripRideType

db_session = session()

coverage_zone = CoverageZone.get_initial(db_session)
user = User.create(
    db_session,
    first_name='Ulyana (High speed)',
    last_name='Smith',
    middle_name='Alone',
    coverage_zone_id=coverage_zone.id
)

trip = Trip.book(
    db_session,
    user_id=user.id,
    transport_id=1,
    coverage_zone_id=coverage_zone.id
)
trip.start(db_session)

trip_ride = TripRide.start(
    db_session,
    trip_id=trip.id,
    ride_type=TripRideType.RIDE,
    initial_speed=90.0
)
sleep(10)
trip_ride.finish(db_session)

trip_ride = TripRide.start(
    db_session,
    trip_id=trip.id,
    ride_type=TripRideType.AWAIT,
)
sleep(1)
trip_ride.finish(db_session)

result: TripFinishResult = trip.finish(db_session, user_id=user.id)
print(result.__dict__)
