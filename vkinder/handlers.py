from vkbottle import GroupEventType, GroupTypes, VKAPIError
from vkbottle.bot import Message
from vkbottle.modules import logger

from . import bot, user
from .messages import hello_message, init_search
from .states import user_data_handler
from .keyboards import keyboard_slider, keyboard_search


@bot.on.private_message(text=['Начать', 'начать'])
async def start_handler(message: Message):
    users_info = await user.api.users.get(message.from_id)
    await message.answer(hello_message.format(users_info[0].first_name), keyboard=keyboard_search)


@bot.on.private_message(text=['Поиск 🔎'])
async def search_handler(message: Message):
    user_id = message.from_id
    users = await user.api.users.get(user_id, fields=['sex', 'city', 'bdate', 'relation'])
    user_info = users[0]

    await message.answer(init_search.format(user_info.first_name))
    await user_data_handler(message)


@bot.on.raw_event(GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
async def group_join_handler(event: GroupTypes.GroupJoin):
    user_id = event.object.user_id
    users_info = await user.api.users.get(user_id)
    user_name = users_info[0].first_name
    try:
        await bot.api.messages.send(peer_id=user_id, message=hello_message.format(user_name), random_id=0,
                                    keyboard=keyboard_search)
    except VKAPIError[901]:
        logger.error('Unable to send a message to a user with the ID {}', user_id)
