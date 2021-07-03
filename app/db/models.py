import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    """ v-solar members user table """
    __tablename__ = 'users'
    id = Column('user_id', Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String, index=True)
    career = Column(String)
    team = Column(String, index=True)
    profile_photo_path = Column(String, unique=True)

    news = relationship('New', back_populates='author')
    announcements = relationship('Announcement', back_populates='author')


class New(Base):
    """ content metadata information """
    __tablename__ = 'news'
    id = Column('new_id', Integer, primary_key=True)
    title = Column(String, unique=True, index=True)
    subtitle = Column(String)
    reading_time = Column(Integer)
    subject = Column(String)
    content_dir = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_edit_at = Column(DateTime, default=datetime.datetime.utcnow)

    author_id = Column(Integer, ForeignKey('users.user_id'))
    author = relationship('User', back_populates='contents')


class Announcement(Base):
    """ announcements in home page """
    __tablename__ = 'announcements'
    id = Column('announcement_id', Integer, primary_key=True)
    title = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_edit_at = Column(DateTime, default=datetime.datetime.utcnow)

    author_id = Column(Integer, ForeignKey('users.user_id'))
    author = relationship('User', back_populates='announcements')


class Donor(Base):
    """ individuals who donate money """
    __tablename__ = 'donors'
    id = Column('donor_id', Integer, primary_key=True)
    name = Column(String, index=True)


class Sponsor(Base):
    """ organizations supporting v-solar """
    __tablename__ = 'sponsors'
    id = Column('sponsor_id', Integer, primary_key=True)
    name = Column(String, unique=True)
    logo_path = Column(String, unique=True)
