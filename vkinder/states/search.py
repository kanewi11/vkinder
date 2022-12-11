from typing import List

from vkbottle import CtxStorage
from vkbottle.bot import Message
from vkbottle.bot import BotLabeler
from vkbottle import BaseStateGroup
from vkbottle import Keyboard, Text, KeyboardButtonColor
from vkbottle_types.codegen.objects import UsersUserFull

from ..models import User
from ..messages import not_found
from ..config import api, SEARCH_USERS_PARAMS, SEARCH_USERS_FIELDS, GET_PHOTOS_PARAMS
from ..utils import get_user, reversed_sex_table


search_labeler = BotLabeler()
ctx = CtxStorage()


class SearchState(BaseStateGroup):
    SEARCH = 0
    NEXT = 1
    LIKE = 2


async def get_user_photos(user_id: int) -> List[str]:
    photos_object = await api.photos.get_all(owner_id=user_id, **GET_PHOTOS_PARAMS)
    photos = photos_object.items
    return [f'photo{photo.owner_id}_{photo.id}' for photo in photos]


async def search_users(user: User) -> List[UsersUserFull]:
    search_params = SEARCH_USERS_PARAMS.copy()
    params = {
        'sex': reversed_sex_table[user.sex_id],
        'hometown': user.city,
        'age_from': user.age,
        'age_to': user.age,
        'status': user.relation_id,
        'fields': SEARCH_USERS_FIELDS,
    }

    search_params.update(params)
    users_object = await api.users.search(**search_params)
    users = users_object.items
    for user in users:
        if user.is_friend or not user.can_write_private_message:
            users.remove(user)
    return users


async def search_state_handler(message: Message):
    user = get_user(message.from_id)
    users = await search_users(user)

    if not users:
        await message.answer(not_found)
        return

    first_user = users[0]
    if len(users) > 1:
        ctx.set('users', users[1:])
        like_button = Text('&#10084;', {'type': 'like', 'user_id': first_user.id})
        next_button = Text('Дальше', {'type': 'next', 'user_id': first_user.id})
        url = f'https://vk.com/id{first_user.id}'
        url_button = Text('Перейти 🔗', {'type': 'open_link', 'link': url})
        keyboard_slider = Keyboard(one_time=True, inline=True)
        keyboard_slider.add(like_button, color=KeyboardButtonColor.NEGATIVE)
        keyboard_slider.add(next_button, color=KeyboardButtonColor.PRIMARY)
        keyboard_slider.add(url_button)
        keyboard_slider.get_json()


@search_labeler.private_message(state=SearchState.LIKE, payload={'type': 'like'})
async def like_handler(message: Message):
    ...


@search_labeler.private_message(state=SearchState.NEXT, payload={'type': 'next'})
async def next_handler(message: Message):
    ...
