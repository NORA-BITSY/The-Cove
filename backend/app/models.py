from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id          = Column(Integer, primary_key=True, index=True)
    fb_id       = Column(String, unique=True, index=True, nullable=False)
    name        = Column(String, nullable=False)
    email       = Column(String, nullable=True)
    badges      = Column(Text, default="")    # << NEW column for badges
    created_at  = Column(DateTime, default=datetime.utcnow)
    spots       = relationship("Spot", back_populates="claimant")
    events      = relationship("Event", back_populates="organizer")

class Spot(Base):
    __tablename__ = "spots"
    id          = Column(Integer, primary_key=True)
    lat         = Column(Float, nullable=False)
    lon         = Column(Float, nullable=False)
    claimed_at  = Column(DateTime)
    note        = Column(Text)
    claimant_id = Column(Integer, ForeignKey("users.id"))
    checked_in  = Column(Boolean, default=False)
    claimant    = relationship("User", back_populates="spots")

class Event(Base):
    __tablename__ = "events"
    id          = Column(Integer, primary_key=True)
    title       = Column(String, nullable=False)
    description = Column(Text)
    start_time  = Column(DateTime, nullable=False)
    end_time    = Column(DateTime, nullable=False)
    location    = Column(String)
    organizer_id= Column(Integer, ForeignKey("users.id"))
    organizer   = relationship("User", back_populates="events")

class Alert(Base):
    __tablename__ = "alerts"
    id          = Column(Integer, primary_key=True)
    alert_type  = Column(String, nullable=False)
    description = Column(Text)
    lat         = Column(Float)
    lon         = Column(Float)
    created_at  = Column(DateTime, default=datetime.utcnow)
    reporter_id = Column(Integer, ForeignKey("users.id"))

class Stream(Base):
    __tablename__ = "streams"
    id          = Column(String, primary_key=True)  # UUID as string
    title       = Column(String, nullable=False)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    active      = Column(Boolean, default=False)
    created_at  = Column(DateTime, default=datetime.utcnow)
    streamer    = relationship("User")

class Message(Base):
    """
    New global message feed.
    """
    __tablename__ = "messages"
    id         = Column(Integer, primary_key=True)
    content    = Column(Text, nullable=False)
    author_id  = Column(Integer, ForeignKey("users.id"), nullable=True)
    timestamp  = Column(DateTime, default=datetime.utcnow)
    # No relationship on User to keep it simple

class Review(Base):
    """
    Stub model for local business ratings.
    """
    __tablename__ = "reviews"
    id             = Column(Integer, primary_key=True)
    business_name  = Column(String, nullable=False)
    rating         = Column(Integer, default=0)
    comment        = Column(Text, default="")
    user_id        = Column(Integer, ForeignKey("users.id"))
    created_at     = Column(DateTime, default=datetime.utcnow)
