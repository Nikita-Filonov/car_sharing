from database import session
from models import Transport

db_session = session()

all_transports = Transport.query(db_session)

for transport in all_transports:
    print(f'{transport.model=}, {transport.brand=}, {transport.transport_level_id=}')


level_transports = Transport.query(db_session, level='intermediate')

for transport in level_transports:
    print(f'{transport.model=}, {transport.brand=}, {transport.transport_level_id=}')


model_transports = Transport.query(db_session, model='A4')

for transport in model_transports:
    print(f'{transport.model=}, {transport.brand=}, {transport.transport_level_id=}')
