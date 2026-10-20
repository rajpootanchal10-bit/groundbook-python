from datetime import date, datetime, timedelta, timezone

class Clock:
    def now(self) -> datetime:
        raise NotImplementedError
    def today(self) -> date:
        return self.now().date()

class SystemClock(Clock):
    def now(self) -> datetime:
        return datetime.now(timezone.utc)

class FixedClock(Clock):
    """A clock a test controls; advance moves it; set pins it."""
    def __init__(self, at: datetime):
        self._at = at

    def now(self) -> datetime:
        return self._at

    def advance(self, **delta) -> datetime:
        self._at = self._at + timedelta(**delta)
        return self._at

# Global module variable instance initialized once
clock = SystemClock()

def get_clock() -> Clock:
    return clock