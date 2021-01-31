from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import start_menu
from keyboards.inline import delete_markup
from loader import dp
from states.photo import Photo
from utils.db_api import Base


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    try:
        admin = Base().read_admin('admins', message.chat.id)
        if admin[1] == 1:
            await message.answer(f'Привет <pre>{message.from_user.full_name}</pre>\n\n'
                                 f'Я <b>бот Решелье 🤖</b>,в котором ты найдешь задания на день',
                                 reply_markup=start_menu)

        else:
            await message.answer(text='Извини но ты не админ!\n')

    except:
        await message.answer(
            f"Привет я Бот Решелье 🤖, который поможет решить твои задачи по:\n"
            f"<b>Математике, геометрии, алгебре и высшей математике 👨‍🏫</b>\n\n"
            f"Первая попытка бесплатная, последующие решения будут стоить 100 рублей. ‍\n\n"
            f"<code>💎 Отправляй фотографию задачи, и я решу её</code>", parse_mode='HTML')

        await Photo.chek_photo.set()


@dp.message_handler(content_types=types.ContentType.ANY, state=Photo.chek_photo)
async def photo_download(message: types.Message, state: FSMContext):
    try:
        download_task = await message.photo[-1].download()
        if len(Base().read_tasks_id('tasks', message.chat.id)) == 1:
            await message.answer('🤓 Извини, но ты уже разместил задание, дождись своей очереди ⭐️')
        else:
            Base().add_task('tasks', message.chat.id, f'{download_task.name}', False)
            await message.answer('✅ Твоё задание отправлено на модерацию, дождись ответа 📬', reply_markup=delete_markup)
            await state.reset_state()
    except:
        await message.answer(text='Отправляй только задание в ввиде фото!')
        await Photo.chek_photo.set()