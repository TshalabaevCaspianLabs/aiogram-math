from aiogram import types

from loader import dp, bot
from utils.db_api import Base
from utils.misc.logging import logger
from keyboards.inline import user_support


@dp.message_handler(content_types=types.ContentType.ANY)
async def p2p(message: types.Message):
    try:
        admin = Base().read_admin('admins', message.chat.id)
        if admin[1] == 1:
            try:
                id = Base().read_tasks('tasks')
                if id[2] == 1:
                    photo = await message.photo[-1].download()
                    file = open(photo.name, 'rb')
                    await bot.send_photo(chat_id=id[0], photo=file)
            except Exception as e:
                logger.error(e)

            try:
                id = Base().read_tasks('tasks')
                if id[2] == 1:
                    text = message.text
                    await bot.send_message(chat_id=id[0], text=text)
            except Exception as e:
                logger.error(e)
    except:
        pass
    try:
        if message.chat.id == Base().read_tasks('tasks')[0]:
            id = Base().read_tasks('tasks')
            if id[2] == 1:
                admin = Base().read_admin_p2p('admins')
                for cheker in admin:
                    if cheker[1] == 1:
                        try:
                            photo = await message.photo[-1].download()
                            file = open(photo.name, 'rb')
                            await bot.send_photo(chat_id=cheker[0], photo=file)
                        except Exception as e:
                            logger.error(e)

                        try:
                            text = message.text
                            await bot.send_message(chat_id=cheker[0], text=text)
                        except Exception as e:
                            logger.error(e)
                    else:
                        pass
    except:
        await message.answer(text='Извини, но тебе нужно использовать кнопки', reply_markup=user_support)