from loader import dp
from aiogram import types
from keyboards.inline import user_support


@dp.message_handler(content_types=types.ContentType.TEXT)
async def send_echo(message: types.Message):
    await message.answer(text='<b>😋 Воспользуйся кнопками бота что бы активировать нужную тебе функцию</b>', reply_markup=user_support)