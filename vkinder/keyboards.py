from vkbottle import Keyboard, Text, KeyboardButtonColor


__all__ = ['keyboard_search']


search_button = Text('Поиск 🔎')
keyboard_search = Keyboard(one_time=True, inline=False)
keyboard_search.add(search_button)
keyboard_search = keyboard_search.get_json()
