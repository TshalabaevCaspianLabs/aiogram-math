from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.default import start_menu
from loader import dp, bot
from states import Admin
from utils.db_api import Base


@dp.message_handler(state=Admin.adm)
async def swap_admin(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(admin=name)
    Base().update_admin('admins', True, name)

    admins = Base().read_admin_p2p('admins')
    for admin in admins:
        if admin[2] == name:
            pass
        else:
            if admin[1] == 1:
                Base().update_admin('admins', False, admin[2])


    id = Base().read_admin_name('admins', name)

    await bot.send_message(chat_id=message.chat.id, text='✅ Ты поменялся ролями', reply_markup=ReplyKeyboardRemove())

    await bot.send_message(chat_id=id, text=f'Привет, тебя назначили админом 🧔 ', reply_markup=start_menu)

    await state.reset_state()
