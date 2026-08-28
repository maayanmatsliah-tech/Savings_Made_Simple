from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# The engine: connects to a SQLite file called "savings.db" in your project root.
# "sqlite:///" is the connection string format SQLAlchemy expects for SQLite.
engine = create_engine("sqlite:///savings.db")

# This is the line that actually creates the tables (goals, weeks) inside
# savings.db, based on every class that inherits from Base in models.py.
# Safe to call every time the app starts — it does nothing if tables already exist.
Base.metadata.create_all(engine)

# sessionmaker builds a "factory" for creating sessions bound to this engine.
# You call SessionLocal() each time you want a fresh session to work with.
SessionLocal = sessionmaker(bind=engine)