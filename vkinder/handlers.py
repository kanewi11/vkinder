from vkbottle.bot import BotLabeler
from vkbottle.bot import Message

from .keyboards import keyboard_slider, keyboard_search
from .messages import hello_message, init_search
from .states import user_data_handler
from .config import api


chat_bot_labeler = BotLabeler()


@chat_bot_labeler.private_message(text=['Начать', 'начать'])
async def start_handler(message: Message):
    users_info = await api.users.get(message.from_id)
    await message.answer(hello_message.format(users_info[0].first_name), keyboard=keyboard_search)


@chat_bot_labeler.private_message(text=['Поиск 🔎'])
async def search_handler(message: Message):
    user_id = message.from_id
    users = await api.users.get(user_id, fields=['sex', 'city', 'bdate', 'relation'])
    user_info = users[0]

    await message.answer(init_search.format(user_info.first_name))
    await user_data_handler(message)
