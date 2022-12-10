from vkbottle import Keyboard, Text, KeyboardButtonColor


__all__ = ['keyboard_slider', 'keyboard_search']


like = Text('&#10084;', {'type': 'like'})
next = Text('Дальше', {'type': 'next'})
keyboard_slider = Keyboard(one_time=True, inline=True)
keyboard_slider.add(like, color=KeyboardButtonColor.NEGATIVE)
keyboard_slider.add(next, color=KeyboardButtonColor.PRIMARY)


search = Text('Поиск 🔎')
keyboard_search = Keyboard(one_time=True, inline=False)
keyboard_search.add(search)
keyboard_search = keyboard_search.get_json()
