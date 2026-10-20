from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Venue(Base):
    __tablename__ = "venues"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    slug = Column(String(32), unique=True, nullable=False)
    name = Column(String(80), nullable=True)

class Ground(Base):
    __tablename__ = "grounds"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    code = Column(String(8), nullable=False)
    name = Column(String(60), nullable=False)
    opens = Column(String(5), nullable=False)
    closes = Column(String(5), nullable=False)
    sunday_opens = Column(String(5), nullable=False)
    sunday_closes = Column(String(5), nullable=False)

class EventType(Base):
    __tablename__ = "event_types"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    code = Column(String(32), nullable=False)
    name = Column(String(80), nullable=False)
    setup_minutes = Column(Integer, default=0, nullable=False)
    teardown_minutes = Column(Integer, default=0, nullable=False)

class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    ground_code = Column(String(8), nullable=False)
    event_code = Column(String(32), nullable=False)
    booking_date = Column(String(10), nullable=False)
    start_time = Column(String(5), nullable=False)
    end_time = Column(String(5), nullable=False)
    state = Column(String(16), default="confirmed", nullable=False)