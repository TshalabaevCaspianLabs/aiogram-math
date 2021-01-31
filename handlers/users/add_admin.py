from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.photo import Admin
from utils.db_api import Base

@dp.message_handler(commands=['add_admin'])
async def add_admin(message: types.Message):
    await message.answer(text='Введи своё имя для записи в базу:')

    await Admin.new_admin.set()


@dp.message_handler(state=Admin.new_admin)
async def new_admin(message: types.Message, state: FSMContext):
    name = message.text
    Base().add_admin('admins', message.chat.id, False, name)

    await message.answer(text='✅ Успешно, жди когда тебя назначат админом!')

    await state.reset_state()