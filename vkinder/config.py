import logging

import sqlalchemy
from vkbottle import API, BuiltinStateDispenser
from vkbottle.bot import BotLabeler
from vkbottle.modules import logger


from config import USER_TOKEN, DSN
from .models import create_tables


logging.basicConfig(level=logging.DEBUG)
logger.setLevel(logging.DEBUG)

engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

api = API(USER_TOKEN)
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()
