from aiogram import types

from keyboards.default import start_menu
from keyboards.inline import user_support
from loader import dp, bot
from utils.db_api import Base


@dp.message_handler(text='Остановить чат ⏰')
async def stop_chat(message: types.Message):
    id = Base().read_tasks('tasks')

    Base().delete_task('tasks', id[0])

    await bot.send_message(chat_id=id[0], text='Надеюсь тебе все понравилось\n\n'
                                               '<b>А если у тебя остались вопросы, то обращайся в нашу службу поддержки</b>',
                           reply_markup=user_support)

    await message.answer(text='Задание успешно выполнено!', reply_markup=start_menu)
