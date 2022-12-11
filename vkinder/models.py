from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    sex_id = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    relation_id = Column(Integer, nullable=False)

    def __init__(self, user_id: int, sex_id: int, age: int, city: str, relation_id: int):
        super().__init__()
        self.user_id = user_id
        self.sex_id = sex_id
        self.age = age
        self.city = city
        self.relation_id = relation_id

    def __repr__(self):
        return f'<{type(self).__name__}(id={self.id})>'


class View(Base):
    __tablename__ = 'view'
    id = Column(Integer, primary_key=True)
    viewed_user_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship(User, backref='views')

    def __init__(self, viewed_user_id: int, user_id: int):
        super().__init__()
        self.viewed_user_id = viewed_user_id
        self.user_id = user_id

    def __repr__(self):
        return f'<{type(self).__name__}(id={self.id})>'


class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    liked_user_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship(User, backref='likes')

    def __init__(self, liked_user_id: int, user_id: int):
        super().__init__()
        self.liked_user_id = liked_user_id
        self.user_id = user_id

    def __repr__(self):
        return f'<{type(self).__name__}(id={self.id})>'


def create_tables(engine: create_engine):
    Base.metadata.create_all(engine)
