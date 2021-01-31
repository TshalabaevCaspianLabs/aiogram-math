from aiogram import types

from keyboards.inline import orsers, admin_panel
from loader import dp
from utils.db_api import Base
from utils.misc.logging import logger


@dp.message_handler(text='Задания 📝')
async def orders(message: types.Message):
    admin = Base().read_admin('admins', message.chat.id)
    if admin[1] == 1:
        try:
            data = Base().read_tasks('tasks')
            file = open(data[1], 'rb')
            await message.answer_photo(photo=file, reply_markup=orsers)
        except Exception as e:
            logger.error(e)
            await message.answer(text='Извини я не нашел заданий в базе 😿')
    else:
        await message.answer(text='Извини но ты не админ!\n'
                                  'В скором времени тебя назначат админом')


@dp.message_handler(text='Админ панель 🤖')
async def admin_panel_(message: types.Message):
    admin = Base().read_admin('admins', message.chat.id)
    if admin[1] == 1:
        await message.answer(text=f'<pre>{message.from_user.full_name} 🧔 </pre>\n\n'
                                  f'<i>Это твоя админ панель, тут ты можешь</i>\n\n'
                                  f'<b>- 👥 Поменять админа</b>\n'
                                  f'<b>- 🌐 Выгрузить базу данных с людьми</b>', reply_markup=admin_panel,
                             parse_mode='html')

    else:
        await message.answer(text='Извини но ты не админ!\n'
                                  'В скором времени тебя назначат админом')
