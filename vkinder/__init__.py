# -*- coding: utf-8 -*-
"""
:authors: kanewi11
:license:  GPL-3.0 license, see LICENSE file

:copyright: (c) 2022 kanewi11
"""

__author__ = 'kanewi11'
__email__ = 'blacknekit11@gmail.com'

from vkbottle.bot import Bot

from .models import create_tables
from .handlers import chat_bot_labeler
from .states import states_bot_labeler, state_dispenser
from .config import state_dispenser, labeler, COMMUNITY_TOKEN


labeler.load(chat_bot_labeler)
labeler.load(states_bot_labeler)

bot = Bot(token=COMMUNITY_TOKEN, labeler=labeler, state_dispenser=state_dispenser)


def run():
    bot.run_forever()
