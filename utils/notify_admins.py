import logging

from aiogram import Dispatcher
from utils.db_api import Base


async def on_startup_notify(dp: Dispatcher):
        admin = Base().read_admin('admins')
        try:
            await dp.bot.send_message(admin, "Бот Запущен")

        except Exception as err:
            logging.exception(err)
