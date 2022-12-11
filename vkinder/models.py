from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    vk_user_id = Column(Integer, nullable=False)
    sex = Column(Integer, nullable=False)
    birthday = Column(DateTime, nullable=False)
    city = Column(String, nullable=False)
    family_status_id = Column(Integer, nullable=False)


class View(Base):
    __tablename__ = 'view'
    id = Column(Integer, primary_key=True)
    viewed_user_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship(User, backref='views')


class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    liked_user_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship(User, backref='likes')


def create_tables(engine: create_engine):
    Base.metadata.create_all(engine)
