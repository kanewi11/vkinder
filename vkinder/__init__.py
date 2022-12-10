# -*- coding: utf-8 -*-
"""
:authors: kanewi11
:license:  GPL-3.0 license, see LICENSE file

:copyright: (c) 2022 kanewi11
"""

__author__ = 'kanewi11'
__email__ = 'blacknekit11@gmail.com'

import logging

from vkbottle.bot import Bot
from vkbottle.modules import logger
from vkbottle.user import User

from config import COMMUNITY_TOKEN, USER_TOKEN


logging.basicConfig(level=logging.DEBUG)
logger.setLevel(logging.DEBUG)


bot = Bot(token=COMMUNITY_TOKEN)
user = User(token=USER_TOKEN)

from .handlers import *


def run():
    bot.run_forever()
