from datetime import date, datetime, timezone
from typing import Annotated, Literal, List
from pydantic import BaseModel, ConfigDict, Field, PlainSerializer

# --- ISO Timestamp Formatting Helper ---
def _iso_z(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4] + "Z"

utc_z = Annotated[datetime, PlainSerializer(_iso_z, return_type=str)]
BookingState = Literal["requested", "confirmed", "cancelled", "expired"]

# --- Grounds list schemas ---
class GroundOut(BaseModel):
    ground: str
    name: str
    opens: str
    closes: str
    sunday_opens: str
    sunday_closes: str

    model_config = ConfigDict(from_attributes=True)

class GroundsOut(BaseModel):
    venue: str
    grounds: List[GroundOut]

# --- Event types list schemas ---
class EventTypeOut(BaseModel):
    code: str
    name: str
    setup_minutes: int
    teardown_minutes: int

    model_config = ConfigDict(from_attributes=True)

class EventTypesOut(BaseModel):
    event_types: List[EventTypeOut]

# --- Day booking schemas ---
class DayBookingOut(BaseModel):
    booking_id: str
    event: str
    from_at: str = Field(..., alias="from")
    to_at: str = Field(..., alias="to")
    ground_held_from: str
    ground_held_to: str
    free: bool
    ground_held: bool
    state: BookingState

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class DayOut(BaseModel):
    venue: str
    ground: str
    date: str
    opens: str
    closes: str
    bookings: List[DayBookingOut]