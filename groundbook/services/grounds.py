from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import Ground, EventType, Venue

def list_grounds(session: Session, venue: Venue) -> list[Ground]:
    return list(session.scalars(select(Ground).where(Ground.venue_id == venue.id).order_by(Ground.code)))

def list_event_types(session: Session, venue: Venue) -> list[EventType]:
    return list(session.scalars(select(EventType).where(EventType.venue_id == venue.id).order_by(EventType.id)))

def hours_for(ground: Ground, day: date) -> tuple[str, str]:
    if day.weekday() == 6:
        return ground.sunday_opens, ground.sunday_closes
    return ground.opens, ground.closes