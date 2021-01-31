from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.misc import logging


async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    logging.info('Bot Started')
    executor.start_polling(dp)
