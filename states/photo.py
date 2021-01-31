from aiogram.dispatcher.filters.state import StatesGroup, State


class Photo(StatesGroup):
    chek_photo = State()


class Admin(StatesGroup):
    adm = State()
    new_admin = State()


class Promo(StatesGroup):
    code = State()