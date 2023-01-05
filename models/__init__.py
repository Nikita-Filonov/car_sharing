from database import Base, engine
from models.coverage_zone import CoverageZone
from models.transport.transport import Transport
from models.transport.transport_level import TransportLevel
from models.trip.trip import Trip
from models.trip.trip_ride import TripRide
from models.user import User

Base.metadata.create_all(engine)
