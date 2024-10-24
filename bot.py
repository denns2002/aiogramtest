import os  # для подгрузки env, который мы бы не хотели отправлять на git

from aiogram import Bot
from dotenv import load_dotenv


load_dotenv()  # подгружаем переменные окружения (windows like)
token = os.environ.get('TOKEN')  # получаем токен бота
bot = Bot(token=token)  # Объект бота
