from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# create database
engine = create_engine("sqlite:///chat.db")

# create session
SessionLocal = sessionmaker(bind=engine)

# base class
Base = declarative_base()

# table
class Chat(Base):

    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)

    user_message = Column(String)

    ai_response = Column(String)


# create table
Base.metadata.create_all(engine)