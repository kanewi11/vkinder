from vkbottle import BaseStateGroup
from vkbottle.bot import Message
from vkbottle import CtxStorage

from . import bot, user
from .utils import get_age, reversed_sex_table, sex_table, relation_table
from config import AGE_FROM, AGE_TO


ctx = CtxStorage()


class UserInfoState(BaseStateGroup):
    USER_DATA = 0
    AGE = 1
    CITY = 2


@bot.on.private_message(state=UserInfoState.AGE)
async def age_handler(message: Message):
    text = message.text.strip()
    if not text.isdigit():
        await message.answer('🔢 Отправь только ци-фо-ры, я программа тупенькая, я тебя не понимать 🫤')
    else:
        age = int(text)
        if AGE_FROM <= age <= AGE_TO:
            ctx.set('age', age)
        else:
            await message.answer(f'🔞 Тут возрастное ограничение от {AGE_FROM} до {AGE_TO} лет.\n')
    await bot.state_dispenser.delete(message.peer_id)
    await user_data_handler(message)


@bot.on.private_message(state=UserInfoState.CITY)
async def city_handler(message: Message):
    text = message.text.strip()
    cities = await user.api.database.get_cities(country_id=1, q=text)
    if cities.items:
        ctx.set('city', text)
    else:
        await message.answer('🌁 Я не знаю такого города, попробуйте заново...')

    await bot.state_dispenser.delete(message.peer_id)
    await user_data_handler(message)


async def user_data_handler(message: Message):
    user_id = message.from_id
    users = await user.api.users.get(user_id, fields=['sex', 'city', 'bdate', 'relation'])
    user_info = users[0]

    age = ctx.get('age')
    if user_info.city:
        ctx.set('city', user_info.city.title)

    city = ctx.get('city')

    bod = user_info.bdate
    if bod:
        broken_bod = bod.strip('.')
        if len(broken_bod) == 3:
            ctx.set('age', get_age(bod))

    if age is None:
        await bot.state_dispenser.set(message.peer_id, UserInfoState.AGE)
        await message.answer('🔢 Введите свой возраст.')
        return

    if city is None:
        await bot.state_dispenser.set(message.peer_id, UserInfoState.CITY)
        await message.answer('🌃 Введите свой город.')
        return

    relation_object = user_info.relation
    relation_id = relation_object.value
    relation_text = relation_table[relation_id]

    sex_object = user_info.sex
    sex_id = sex_object.value
    reversed_sex_id = reversed_sex_table[sex_id]
    sex_text = sex_table[reversed_sex_id]

    if age and city:
        await message.answer(f'Нужные данные для поиска получены!\n\n'
                             f'Город поиска: {city.title()}\n'
                             f'Возраст примерно: {age}\n'
                             f'Пол: {sex_text}\n'
                             f'Семейное положение: {relation_text}\n\n'
                             f'🔦 Подбираю пару...')
