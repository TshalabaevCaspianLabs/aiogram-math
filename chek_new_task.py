from loader import dp
from keyboards.inline import orsers
import time
from utils.db_api import Base
from utils.misc.logging import logger
import asyncio

async def chek_task(Dispatcher: dp):
    while True:
        try:
            task = Base().read_tasks('tasks')
            file_name = Base().read_notif('notifications')

            if task[1] in file_name:
                logger.debug('[--] SLEEPING 5 SEC')
                time.sleep(5)


            else:
                logger.info('[--] NOTIFICATION ADMIN')
                admins = Base().read_admin_p2p('admins')
                for admin in admins:
                    if admin[1] == 1:

                        file_ = open(task[1], 'rb')
                        await Dispatcher.bot.send_photo(chat_id=admin[0], photo=file_, reply_markup=orsers)
                        Base().add_file_name('notifications', task[1])


        except:
            logger.debug('[--] SLEEPING 5 SEC')
            time.sleep(5)



asyncio.run(chek_task(dp))