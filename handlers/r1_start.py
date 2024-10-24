"""
Все команды, которые может использовать бот, при запуске используются в файле
handlers для привязки к хэндлерам
"""
import logging

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from models import *


log = logging.getLogger(__name__)  # берем уже созданный в main логгер
router_1 = Router()  # роутер для добавления инфы в бд


@router_1.message(Command("start"))
async def cmd_start(message: types.Message):
    # сразу добавляем пользоваеля в бд, если его нет
    with db:
        telegram_id = message.from_user.id  # берем его тг id
        user = User.select().where(User.telegram_id == telegram_id)  # проверяем, есть ли он в нашей базе
        if not user:
            name = message.from_user.username  # берем имя
            User.create(name=name, telegram_id=telegram_id)  # добавляем в нашу бд
            log.info(f'user {telegram_id} | {name} created!')  # логируем, что добавили его

    answer = "Привет, Саша, это тестовый бот, которого я написал для нашего " \
             "урока. :)\nЗдесь базовые функции самого aiogram, работа с ORM " \
             "Peewee."

    kb = ReplyKeyboardBuilder()  # создаем кнопочки меню
    kb.button(text="Добавить")
    kb.button(text="Пустышка")
    kb.button(text="История")
    kb = kb.as_markup(resize_keyboard=True)

    await message.answer(answer, reply_markup=kb)


# форма для ввода (например параметров поиска)
class AddForm(StatesGroup):
    first = State()
    second = State()
    third = State()


# Вариант из меню - Добавить и ввод первого поля формы
@router_1.message(F.text.lower() == "добавить")  # F - фильтр
async def start_add_form(message: Message, state: FSMContext):
    """Типа что-то ищем и работаем с формой"""
    with db:
        # берем пользователя из нашей бд по его тг id
        user = User.select().where(User.telegram_id == message.from_user.id)
        if user:
            # включаем ввод поля first из формы
            await state.set_state(AddForm.first)
            await message.answer("Введите первое поле:")

        else:
            answer = "Выполните команду /start, чтобы пользоваться ботом!"
            await message.answer(answer)


# Продолжаем ввод формы и вводим второе поле
@router_1.message(AddForm.first)  # после ввода первого поля
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(first=message.text)  # обноавляем значние first в форме
    await state.set_state(AddForm.second)  # Переключаем форму на ввод second поля
    await message.answer("Введите второе поле:")


# Продолжаем ввод формы и вводим третье поле
@router_1.message(AddForm.second)  # после ввода первого поля
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(second=message.text)  # обноавляем значние second в форме
    await state.set_state(AddForm.third)  # Переключаем форму на ввод third поля
    await message.answer("Введите третье поле:")


# Заканчиваем ввод и схраняем результат в БД
@router_1.message(AddForm.third)  # после ввода первого поля
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(third=message.text)  # обноавляем значние third в форме
    data = await state.get_data()  # собираем все данные с формы, чтобы потом их использовать
    await state.clear()  # очищаем формочку

    # добавляем запись в бд
    with db:
        # берем пользоваля, чтобы привязать запись истории к нему
        user = User.select().where(User.telegram_id == message.from_user.id)
        if user:
            SearchRequest.create(
                user=user,  # привяызываем запись истории к пользователю
                first=data["first"],
                second=data["second"],
                third=data["third"],
            )

    await message.answer("Запись в вашу историю добавленна!")


# Вариант из меню - Пустышка.
@router_1.message(F.text.lower() == "пустышка")  # F - фильтр
async def answer_space(message: types.Message):
    """Типа что-то ищем и работаем ORM Peewee"""
    answer = """
        Просто пустышка, которая дает выбор...
    """
    await message.answer(answer)


# Вариант из меню - История.
@router_1.message(F.text.lower() == "история")  # F - фильтр
async def check_hisory(message: types.Message):
    """История запросов"""

    with db:
        # берем пользователя из нашей бд по его тг id
        user = User.select().where(User.telegram_id == message.from_user.id)
        if user:
            answer = 'История:\n'
            history = SearchRequest.select().where(  # берем всю историю пользователя
                SearchRequest.user == user  # филтруем по id пользователя
            )
            for row in history:  # перебираем все записи
                answer += f"{row.first} {row.second} {row.third}\n"  # добавляем в ответ

        else:
            answer = "Выполните команду /start, чтобы пользоваться ботом!"

    await message.answer(answer)
