import logging

from vkbottle import GroupEventType, GroupTypes, VKAPIError
from vkbottle.bot import BotLabeler
from vkbottle.bot import Message

from .keyboards import keyboard_search
from .messages import hello, init_search, search
from .states.user_data import data_state_handler
from .states.search import search_state_handler
from .config import api, state_dispenser


chat_bot_labeler = BotLabeler()


@chat_bot_labeler.private_message(text=['Начать', 'начать'])
async def start_handler(message: Message):
    users = await api.users.get(message.from_id)
    user_info = users[0]
    await message.answer(hello.format(user_info.first_name), keyboard=keyboard_search)


@chat_bot_labeler.private_message(text=['Поиск 🔎'])
async def search_handler(message: Message):
    users = await api.users.get(message.from_id)
    user_info = users[0]

    await message.answer(init_search.format(user_info.first_name))
    await data_state_handler(message)
    await search_state_handler(message)


@chat_bot_labeler.raw_event(GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
async def group_join_handler(event: GroupTypes.GroupJoin):
    try:
        await api.messages.send(peer_id=event.object.user_id, message=hello, random_id=0)
    except VKAPIError[901]:
        logging.warning('Unable to send a message to a user with the ID {0}'.format(event.object.user_id))
