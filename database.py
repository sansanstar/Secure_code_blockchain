import json

from sqlalchemy import Column, DateTime, Integer, PickleType, String, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker


# Set up the Database
engine = create_engine('sqlite:///electron.db')
db = scoped_session(sessionmaker(bind=engine))


class BaseModel(object):
    @declared_attr
    def __tablename__(self):
        """
        Ensures all tables have the same name as their models (below)
        """
        return self.__name__.lower()

    def to_dict(self):
        """
        Helper method to convert any database row to dict
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_json(self):
        """
        Helper method to convert any database row to JSON
        """
        return json.dumps(self.to_dict(), sort_keys=True)


Base = declarative_base(cls=BaseModel)


class Peer(Base):
    identifier = Column(String(32), primary_key=True)
    hostname = Column(String, index=True, unique=True)


class Block(Base):
    height = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, index=True)
    transactions = Column(PickleType)
    previous_hash = Column(String(64))
    proof = Column(String(64))
    hash = Column(String(64))


class Config(Base):
    key = Column(String(64), primary_key=True, unique=True)
    value = Column(PickleType)


def reset_db():
    """
    Drops and Re-creates the Database
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
