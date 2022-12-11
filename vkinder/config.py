import os
import logging

import sqlalchemy
from vkbottle import API, BuiltinStateDispenser
from vkbottle.bot import BotLabeler
from vkbottle.modules import logger

from .models import create_tables


COMMUNITY_TOKEN = os.getenv('COMMUNITY_TOKEN')

# In this link the necessary scope is already passed, replace client_id to get the token
# https://oauth.vk.com/authorize?client_id=1&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,photos,offline&response_type=token&v=5.131&state=123456
USER_TOKEN = os.getenv('USER_TOKEN')

DSN = 'sqlite:///vkinder.db'

AGE_FROM = 16
AGE_TO = 50

USER_DATA_FIELDS = ['sex', 'city', 'bdate', 'relation']
SEARCH_USERS_PARAMS = {
    'offset': 0,
    'count': 1000,
    'city': None,
    'sex': None,
    'age_from': None,
    'age_to': None,
    'has_photo': 1,
    'status': None
}
SEARCH_USERS_FIELDS = ['is_friend', 'can_write_private_message']
GET_PHOTOS_PARAMS = {
    'count': 3,
    'skip_hidden': 1
}

logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.WARNING)

engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

api = API(USER_TOKEN)
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()
