from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True)
    starting_money = Column(Float, nullable=False)
    finishing_money = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    weeks = relationship("Week", back_populates="goal")

class Week(Base):
    __tablename__ = "weeks"

    id = Column(Integer, primary_key=True)
    goal_id = Column(Integer, ForeignKey("goals.id"))
    week_number = Column(Integer, nullable=False)
    money_spent = Column(Float, nullable=False)
    remaining_budget = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    goal = relationship("Goal", back_populates="weeks")