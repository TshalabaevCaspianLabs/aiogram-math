from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.default import stop_chat
from keyboards.inline import filter
from keyboards.inline import orsers, add_task_user, delete_markup
from loader import dp, bot
from sale_chek import sale_chek_qiwi
from states.photo import Photo, Admin, Promo
from utils.db_api import Base


@dp.callback_query_handler(filter.filter(item_name='delete_task'))
async def delete_user_task(call: types.CallbackQuery):
    id = Base().read_tasks('tasks')
    admins = Base().read_admin_p2p('admins')
    for admin in admins:
        if call.message.chat.id == admin[0]:
            Base().delete_task('tasks', id[0])
            await call.message.answer(text='✅ Задание удалено')
            await bot.send_message(chat_id=id[0], text='<b>😿 Твое задание удалали, из-за длительной не оплаты</b>',
                                   reply_markup=add_task_user)

        else:
            if id[0] == call.message.chat.id:
                Base().delete_task('tasks', call.message.chat.id)
                await call.message.delete()
                await call.message.answer(f'✅ Твое задание удалено успешно!', reply_markup=add_task_user)
                admins = Base().read_admin_p2p('admins')
                for admin in admins:
                    if admin[1] == 1:
                        await bot.send_message(chat_id=admin[0],
                                               text='<b>🙈 Заказчик удалил задание, приступай к следующему</b>')
    await call.message.delete()

@dp.callback_query_handler(filter.filter(item_name='send_base'))
async def upload_base(call: types.CallbackQuery):
    file = open('user_pay.db', 'rb')
    await call.message.answer_document(document=file)
    



@dp.callback_query_handler(filter.filter(item_name='yes'))
async def yes_task(call: types.CallbackQuery):
    id = Base().read_tasks('tasks')
    await call.message.delete()
    try:
        if Base().read_user_pay_id('user_pay', id[0])[1] == 0:
            com = Base().read_tasks('tasks')
            user_pay = InlineKeyboardMarkup()

            sale = InlineKeyboardButton(text='💵 Произвести оплату',
                                        url=f'https://qiwi.com/payment/form/99?blocked%5B0%5D=account&amountFraction=0&extra%5B%27account%27%5D=+79119009060&extra%5B%27comment%27%5D={com[1]}&amountInteger=100&blocked%5B1%5D=comment&cment&currency=RUB')
            chek_sale = InlineKeyboardButton(text='💎 Проверить оплату', callback_data=filter.new('chek_sale'))
            promo = InlineKeyboardButton(text='🔵 Использовать промокод', callback_data=filter.new('use_promo'))
            delete_task = InlineKeyboardButton(text='❌ Удалить задание', callback_data=filter.new('delete_task'))
            user_pay.add(sale, chek_sale)
            user_pay.add(promo)
            user_pay.add(delete_task)

            await bot.send_message(chat_id=id[0], text='⭐️ Ты уже использовал пробный раз\n\n'
                                                       '<b>Произведи оплату по кнокпе <i>💵 Произвести оплату</i></b>\n\n'
                                                       '<b>После оплаты нажми на кнопку <i>💎 Проверить оплату</i></b>\n\n'
                                                       '😍 Ты можешь поделиться с другом своим промокодом, и тебе начислят бесплатное решение задачи 🍒\n\n'
                                                       f'<i>Твой промокод <b>{id[0]}</b></i>\n\n'
                                                       '<pre>💞 А если у тебя есть промокод твоего знакомого, то нажимай кнопку</pre>',
                                   reply_markup=user_pay)

            await call.message.answer(text='<i>👨 Ждем оплаты заказчика!</i>\n\n'
                                           '<pre>После оплаты заказчика, вас перенаправят в закрытый чат 📣</pre>',
                                      reply_markup=delete_markup)

        if Base().read_user_pay_id('user_pay', id[0])[1] > 0:
            count = Base().read_user_pay_id('user_pay', id[0])[1]
            Base().update_user_pay('user_pay', id[0], int(count) - 1)
            await bot.send_message(chat_id=id[0], text='✅ Твое задание прошло модерацию\n\n'
                                                       '<b><pre>Ты находишься в закрытом чате с исполнителем напиши ему сообщение</pre></b>')

            await call.message.answer(
                text='<b><pre>Ты находишься в закрытом чате с заказчиком напиши ему сообщение</pre></b>',
                reply_markup=stop_chat)
            Base().update_task_id('tasks', True, id[0])


    # если в базе не нашли запись использования пробного раза
    except Exception as e:
        print(e)

        await bot.send_message(chat_id=id[0], text='✅ Твое задание прошло модерацию\n\n'
                                                   '<b><pre>Ты находишься в закрытом чате с исполнителем напиши ему сообщение</pre></b>')

        await call.message.answer(
            text='<b><pre>Ты находишься в закрытом чате с заказчиком напиши ему сообщение</pre></b>',
            reply_markup=stop_chat)
        Base().add_user_pay('user_pay', id[0], 0)
        Base().update_task_id('tasks', True, id[0])


@dp.callback_query_handler(filter.filter(item_name='no'))
async def no_task(call: types.CallbackQuery):
    # users message
    id = Base().read_tasks('tasks')
    await call.message.delete()
    await bot.send_message(chat_id=id[0], text='❌ Твое задание не прошло модерацию\n\n'
                                               '<pre>Перейди в главное меню и отправь задание снова 🖼</pre>',
                           reply_markup=add_task_user)

    # admins message
    Base().delete_task('tasks', id[0])
    try:
        data = Base().read_tasks('tasks')
        file = open(data[1], 'rb')
        await call.message.answer_photo(photo=file, reply_markup=orsers)
    except:
        await call.message.answer(text='Извини я не нашел заданий в базе 😿')


@dp.callback_query_handler(filter.filter(item_name='add_new_order'))
async def update_task(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(text='<b>Отправь мне новое задание 🆕</b>')
    await Photo.chek_photo.set()


@dp.callback_query_handler(filter.filter(item_name='swap_admin'))
async def swap_admin(call: types.CallbackQuery):
    admins = Base().read_admin_p2p('admins')
    for admin in admins:
        if admin[1] == 1:

            admins_ = Base().read_admin_p2p('admins')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for admin_ in admins_:
                btn = types.KeyboardButton(text=f'{admin_[2]}')
                markup.add(btn)

            await bot.send_message(chat_id=call.message.chat.id, text='Выбери Админа 🧔', reply_markup=markup)
            await Admin.adm.set()
            await call.message.delete()
            await call.message.delete()


@dp.callback_query_handler(filter.filter(item_name='chek_sale'))
async def chek_pay(call: types.CallbackQuery):
    indif = sale_chek_qiwi()
    await call.message.delete()
    if len(indif) == 0:
        com = Base().read_tasks('tasks')
        user_pay = InlineKeyboardMarkup()

        sale = InlineKeyboardButton(text='💵 Произвести оплату',
                                    url=f'https://qiwi.com/payment/form/99?blocked%5B0%5D=account&amountFraction=0&extra%5B%27account%27%5D=+79119009060&extra%5B%27comment%27%5D={com[1]}&amountInteger=100&blocked%5B1%5D=comment&cment&currency=RUB')
        chek_sale = InlineKeyboardButton(text='💎 Проверить оплату', callback_data=filter.new('chek_sale'))
        promo = InlineKeyboardButton(text='🔵 Использовать промокод', callback_data=filter.new('use_promo'))
        delete_task = InlineKeyboardButton(text='❌ Удалить задание', callback_data=filter.new('delete_task'))
        user_pay.add(sale, chek_sale)
        user_pay.add(promo)
        user_pay.add(delete_task)

        id = Base().read_tasks('tasks')
        await bot.send_message(chat_id=id[0], text='<b>❌ Извини, я не увидел оплату</b>\n\n'
                                                   '<i>Попробуй еще раз 😋</i>', reply_markup=user_pay)

    if len(indif) > 0:
        id = Base().read_tasks('tasks')
        await bot.send_message(chat_id=id[0], text='✅ Оплата прошла успешно\n\n'
                                                   '<b><pre>Ты находишься в закрытом чате с исполнителем напиши ему сообщение</pre></b>')

        admins = Base().read_admin_p2p('admins')
        for admin in admins:
            if admin[1] == 1:
                await bot.send_message(
                    chat_id=admin[0],
                    text='<b><pre>Ты находишься в закрытом чате с заказчиком напиши ему сообщение</pre></b>',
                    reply_markup=stop_chat)
                Base().update_task_id('tasks', True, id[0])


@dp.callback_query_handler(filter.filter(item_name='use_promo'))
async def promocod(call: types.CallbackQuery):
    await call.message.answer(text='Введите свой промокод:')
    await Promo.code.set()



@dp.message_handler(state=Promo.code)
async def chek_promo(message: types.Message, state: FSMContext):
    user_code = message.text
    code_in_base = Base().read_user_pay('user_pay')
    data = []
    for cod in code_in_base:
        data.append(cod[0])
    print(data)

    if int(user_code):
        if int(user_code) in data:
            try:
                if message.chat.id == int(user_code):
                    com = Base().read_tasks('tasks')
                    user_pay = InlineKeyboardMarkup()

                    sale = InlineKeyboardButton(text='💵 Произвести оплату',
                                                url=f'https://qiwi.com/payment/form/99?blocked%5B0%5D=account&amountFraction=0&extra%5B%27account%27%5D=+79119009060&extra%5B%27comment%27%5D={com[1]}&amountInteger=100&blocked%5B1%5D=comment&cment&currency=RUB')
                    chek_sale = InlineKeyboardButton(text='💎 Проверить оплату', callback_data=filter.new('chek_sale'))
                    promo = InlineKeyboardButton(text='🔵 Использовать промокод', callback_data=filter.new('use_promo'))
                    delete_task = InlineKeyboardButton(text='❌ Удалить задание', callback_data=filter.new('delete_task'))
                    user_pay.add(sale, chek_sale)
                    user_pay.add(promo)
                    user_pay.add(delete_task)
                    await message.answer(text='<b>Свой промокод использовать нельзя 😎</b>', reply_markup=user_pay)

                else:
                    code = Base().read_promocod('promocod', message.chat.id)
                    if int(user_code) in code:
                        com = Base().read_tasks('tasks')
                        user_pay = InlineKeyboardMarkup()
                        sale = InlineKeyboardButton(text='💵 Произвести оплату',
                                                    url=f'https://qiwi.com/payment/form/99?blocked%5B0%5D=account&amountFraction=0&extra%5B%27account%27%5D=+79119009060&extra%5B%27comment%27%5D={com[1]}&amountInteger=100&blocked%5B1%5D=comment&cment&currency=RUB')
                        chek_sale = InlineKeyboardButton(text='💎 Проверить оплату', callback_data=filter.new('chek_sale'))
                        promo = InlineKeyboardButton(text='🔵 Использовать промокод', callback_data=filter.new('use_promo'))
                        delete_task = InlineKeyboardButton(text='❌ Удалить задание',
                                                           callback_data=filter.new('delete_task'))
                        user_pay.add(sale, chek_sale)
                        user_pay.add(promo)
                        user_pay.add(delete_task)
                        await message.answer('❌ Извини но ты уже использовал этот код', reply_markup=user_pay)


                    else:
                        count = Base().read_user_pay_id('user_pay', user_code)
                        Base().update_user_pay('user_pay', user_code, int(count[1]) + 1)
                        await bot.send_message(chat_id=user_code, text=f'Твой промокод активировали у тебя бесплатных попыток: <b>{int(count[1])+1}</b>')
                        Base().add_promocod('promocod', message.chat.id, user_code)
                        id = Base().read_tasks('tasks')
                        await bot.send_message(chat_id=id[0], text='✅ Промокод активирован\n\n'
                                                                   '<b><pre>Ты находишься в закрытом чате с исполнителем напиши ему сообщение</pre></b>')

                        admins = Base().read_admin_p2p('admins')
                        for admin in admins:
                            if admin[1] == 1:
                                await bot.send_message(
                                    chat_id=admin[0],
                                    text='<b><pre>Ты находишься в закрытом чате с заказчиком напиши ему сообщение</pre></b>',
                                    reply_markup=stop_chat)
                                Base().update_task_id('tasks', True, id[0])

            except Exception as e:
                print(e)
                pass

        # если бот не нашел промокод в базе

        else:
            com = Base().read_tasks('tasks')
            user_pay = InlineKeyboardMarkup()

            sale = InlineKeyboardButton(text='💵 Произвести оплату',
                                        url=f'https://qiwi.com/payment/form/99?blocked%5B0%5D=account&amountFraction=0&extra%5B%27account%27%5D=+79119009060&extra%5B%27comment%27%5D={com[1]}&amountInteger=100&blocked%5B1%5D=comment&cment&currency=RUB')
            chek_sale = InlineKeyboardButton(text='💎 Проверить оплату', callback_data=filter.new('chek_sale'))
            promo = InlineKeyboardButton(text='🔵 Использовать промокод', callback_data=filter.new('use_promo'))
            delete_task = InlineKeyboardButton(text='❌ Удалить задание', callback_data=filter.new('delete_task'))
            user_pay.add(sale, chek_sale)
            user_pay.add(promo)
            user_pay.add(delete_task)
            await message.answer(text='❌ Извини но я нешел такой промокод', reply_markup=user_pay)


        await state.reset_state()

    else:
        com = Base().read_tasks('tasks')
        user_pay = InlineKeyboardMarkup()

        sale = InlineKeyboardButton(text='💵 Произвести оплату',
                                    url=f'https://qiwi.com/payment/form/99?blocked%5B0%5D=account&amountFraction=0&extra%5B%27account%27%5D=+79119009060&extra%5B%27comment%27%5D={com[1]}&amountInteger=100&blocked%5B1%5D=comment&cment&currency=RUB')
        chek_sale = InlineKeyboardButton(text='💎 Проверить оплату', callback_data=filter.new('chek_sale'))
        promo = InlineKeyboardButton(text='🔵 Использовать промокод', callback_data=filter.new('use_promo'))
        delete_task = InlineKeyboardButton(text='❌ Удалить задание', callback_data=filter.new('delete_task'))
        user_pay.add(sale, chek_sale)
        user_pay.add(promo)
        user_pay.add(delete_task)

        await message.answer(text='Извини но ты ввел но числовой код, промокоды только числа, попробуй снова', reply_markup=user_pay)
        await Promo.code.set()