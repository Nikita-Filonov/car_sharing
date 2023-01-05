from sqlalchemy import select

from database import session


def create_with_ensure_exists(entity, payload: list[dict], **kwargs):
    db_session = session()

    for entity_payload in payload:
        result = db_session.execute(
            select(entity).filter_by(**entity_payload, **kwargs)
        )
        is_exists = result.scalars().all()

        if is_exists:
            continue

        model = entity(**entity_payload, **kwargs)
        db_session.add(model)
        db_session.commit()
