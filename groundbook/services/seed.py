import csv
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import EventType, Ground, Venue

def seed(session: Session, seed_dir: str) -> None:
    VENUE_DATA = ("deccan", "Deccan Sports Complex")
    venue = session.scalar(select(Venue).where(Venue.slug == VENUE_DATA[0]))
    if venue is None:
        venue = Venue(slug=VENUE_DATA[0], name=VENUE_DATA[1])
        session.add(venue)
        session.flush()

    venue_id = venue.id

    grounds_file = Path(seed_dir) / "grounds.csv"
    if grounds_file.exists():
        with open(grounds_file, mode="r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                existing = session.scalar(select(Ground).where(Ground.venue_id == venue_id, Ground.code == row["code"]))
                if existing is None:
                    session.add(Ground(
                        venue_id=venue_id, code=row["code"], name=row["name"],
                        opens=row["opens"], closes=row["closes"],
                        sunday_opens=row["sunday_opens"], sunday_closes=row["sunday_closes"]
                    ))

    event_types_file = Path(seed_dir) / "event_types.csv"
    if event_types_file.exists():
        with open(event_types_file, mode="r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                existing = session.scalar(select(EventType).where(EventType.venue_id == venue_id, EventType.code == row["code"]))
                if existing is None:
                    session.add(EventType(
                        venue_id=venue_id, code=row["code"], name=row["name"],
                        setup_minutes=int(row["setup_minutes"]), teardown_minutes=int(row["teardown_minutes"])
                    ))
    session.commit()

def seed_database(session: Session) -> None:
    from ..settings import settings
    seed(session, settings.seed_dir)