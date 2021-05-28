import datetime
import enum

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    """ v-solar members user table """
    __tablename__ = 'users'
    id = Column('user_id', Integer, primary_key=True, index=True)
    username = Column('username', String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    profile_photo_path = Column(String, unique=True)
    career = Column(String, index=True)
    role = Column(String)
    contents = relationship('Content')


class Donor(Base):
    """ table for individuals who donate money """
    __tablename__ = 'donors'
    id = Column('donor_id', Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    logo_path = Column(String, unique=True)


class Sponsor(Base):
    """
    table for organizations supporting v-solar with
    any kind of resources
    """
    __tablename__ = 'sponsors'
    id = Column('sponsor_id', Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    logo_path = Column(String, unique=True)


class ContentEnum(enum.Enum):
    video = 0
    blog = 1
    news = 2
    update = 3


class Content(Base):
    """ content metadata information """
    __tablename__ = 'contents'
    id = Column('content_id', Integer, primary_key=True, index=True)
    content_dir = Column(String, unique=True)
    author_id = Column(Integer, ForeignKey('users.user_id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_edit_at = Column(DateTime)
    type = Column(Enum(ContentEnum), index=True)
