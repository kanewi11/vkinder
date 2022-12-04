from datetime import datetime

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from .users import Users
from config import USER_TOKEN, COMMUNITY_TOKEN


vk = vk_api.VkApi(token=COMMUNITY_TOKEN)
poll = VkLongPoll(vk)


def send_message(user_id, message):
    random_id = int(datetime.now().timestamp() * 100000)
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': random_id,
    })


def events(handlers: dict):
    for event in poll.listen():
        if event.type != VkEventType.MESSAGE_NEW:
            continue

        if not event.to_me:
            continue

        request = event.text

        handler = handlers.get(request)
        if not handler:
            send_message(event.user_id, f'Я не понял 🫤')
            continue
        handler(event.user_id)
