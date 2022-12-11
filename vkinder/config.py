import os
import logging

import sqlalchemy
from vkbottle import API, BuiltinStateDispenser
from vkbottle.bot import BotLabeler
from vkbottle.modules import logger

from .models import create_tables


COMMUNITY_TOKEN = os.getenv('COMMUNITY_TOKEN')
USER_TOKEN = os.getenv('USER_TOKEN')
DSN = 'sqlite:///vkinder.db'

AGE_FROM = 16
AGE_TO = 50

logging.basicConfig(level=logging.DEBUG)
logger.setLevel(logging.DEBUG)

engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

api = API(USER_TOKEN)
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()
