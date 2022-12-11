import datetime
import logging

from sqlalchemy import exc
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import sessionmaker

from .config import engine, api
from .models import User, Like, View


Session = sessionmaker(bind=engine)


sex_table = {
    0: 'любой',
    1: 'женский',
    2: 'мужской',
}

reversed_sex_table = {
    1: 2,
    2: 1,
}

relation_table = {
    0: 'не указано',
    1: 'не женат (не замужем)',
    2: 'встречается',
    3: 'помолвлен(-а)',
    4: 'женат (замужем)',
    5: 'всё сложно',
    6: 'в активном поиске',
    7: 'влюблен(-а)',
    8: 'в гражданском браке',
}


def session_add(cls: object) -> None:
    session = Session()
    try:
        session.add(cls)
        session.commit()
    except exc.SQLAlchemyError as error:
        session.rollback()
        logging.critical(error.__str__())
    finally:
        session.close()


def get_age(date: str) -> int:
    date_object = datetime.datetime.strptime(date, '%d.%m.%Y')
    today = datetime.date.today()
    return relativedelta(today, date_object).years


def is_there_a_user(user_id: int) -> bool:
    with Session() as session:
        users = session.query(User).filter(User.user_id == user_id).all()
    return True if users else False


def get_user(user_id: int) -> User:
    with Session() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
    return user


def add_new_user(user_id: int, age: int, sex_id: int, relation_id: int, city: str) -> None:
    user = User(user_id=user_id, age=age, sex_id=sex_id, city=city, relation_id=relation_id)
    session_add(user)


def add_view(user_id: int, viewed_user_id: int) -> None:
    view = View(user_id=user_id, viewed_user_id=viewed_user_id)
    session_add(view)


def add_like(user_id: int, liked_user_id: int) -> None:
    like = Like(user_id=user_id, liked_user_id=liked_user_id)
    session_add(like)
