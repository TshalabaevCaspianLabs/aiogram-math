from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, bot


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
    await bot.send_photo(message.chat.id,
                         photo='https://sun9-60.userapi.com/impg/c854124/v854124253/248c05/iz-LFXskFTc.jpg?size=1920x1920&quality=96&proxy=1&sign=810dd1b4b06802fa4508b411b2205afe&type=album',
                         caption='Это его <code>template</code>')