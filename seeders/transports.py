import json

from database import session
from models import CoverageZone, Transport, TransportLevel
from seeders.utils import create_with_ensure_exists

BASE_PATH = './seeders/dumps'
transports = json.loads(open(f'{BASE_PATH}/transports.json').read())
transport_levels = json.loads(
    open(f'{BASE_PATH}/transport_levels.json').read()
)


def seed_transports():
    db_session = session()
    coverage_zone = CoverageZone.get_initial(db_session)

    create_with_ensure_exists(TransportLevel, transport_levels)
    create_with_ensure_exists(
        Transport,
        transports,
        coverage_zone_id=coverage_zone.id
    )


if __name__ == '__main__':
    seed_transports()
