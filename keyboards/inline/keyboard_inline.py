from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db_api import Base
from .filter import filter

delete_markup = InlineKeyboardMarkup()
delete_task = InlineKeyboardButton(text='Удалить задание', callback_data=filter.new('delete_task'))
delete_markup.add(delete_task)

orsers = InlineKeyboardMarkup()
yes = InlineKeyboardButton(text='✅ Пример', callback_data=filter.new('yes'))
no = InlineKeyboardButton(text='❌ Не пример', callback_data=filter.new('no'))
orsers.add(yes, no)

user_support = InlineKeyboardMarkup()
add_new_order = InlineKeyboardButton(text='✅ Добавить новое задание', callback_data=filter.new('add_new_order'))
support = InlineKeyboardButton(text='🤖 Связаться с поддержкой', url='https://t.me/leonov_mikhail')
user_support.add(add_new_order)
user_support.add(support)


add_task_user = InlineKeyboardMarkup()
add_task_user.add(add_new_order)


admin_panel = InlineKeyboardMarkup()
swap_admin = InlineKeyboardButton(text='👥 Поменять админа', callback_data=filter.new('swap_admin'))
send_base = InlineKeyboardButton(text='🌐 Выгрузить базу', callback_data=filter.new('send_base'))
admin_panel.add(swap_admin)
admin_panel.add(send_base)







