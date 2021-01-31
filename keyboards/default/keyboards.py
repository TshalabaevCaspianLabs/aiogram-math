from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Задания 📝'),
            KeyboardButton(text='Админ панель 🤖')
        ]
    ],
    resize_keyboard=True
)

stop_chat = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Остановить чат ⏰'),

        ]
    ],
    resize_keyboard=True
)