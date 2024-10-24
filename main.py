"""
Основной файл запуска (точка входа в программу) бота.

Полезные ссылки:
https://mastergroosha.github.io/aiogram-3-guide/messages/
https://mastergroosha.github.io/aiogram-3-guide/routers/#routers
https://mastergroosha.github.io/aiogram-3-guide/buttons/

Формы:
https://stackoverflow.com/questions/69846020/how-to-wait-for-user-reply-in-aiogram
https://docs.aiogram.dev/en/latest/dispatcher/finite_state_machine/index.html

Peewee start:
https://docs.peewee-orm.com/en/latest/peewee/quickstart.html
https://magnetic-evergreen-187.notion.site/ORM-peewee-6a8138e1836e4cbe9a44e4fbaa49e5a1
"""

import asyncio  # поскольку фрейморк асинхронный, нам нужен asyncio
import logging  # логирование

from aiogram import Dispatcher

from bot import bot
from handlers.r1_start import router_1
from handlers.r_unknown import router_unknow


logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w')  # Логирование информации
"""
params:

level - уровень начала логирования

Debug (10): самый низкий уровень логирования, предназначенный для отладочных 
сообщений, для вывода диагностической информации о приложении.

Info (20): этот уровень предназначен для вывода данных о фрагментах кода, 
работающих так, как ожидается.

Warning (30): этот уровень логирования предусматривает вывод предупреждений, 
он применяется для записи сведений о событиях, на которые программист обычно 
обращает внимание. Такие события вполне могут привести к проблемам при работе 
приложения. Если явно не задать уровень логирования — по умолчанию используется
именно warning.

Error (40): этот уровень логирования предусматривает вывод сведений об 
ошибках — о том, что часть приложения работает не так как ожидается, о том, 
что программа не смогла правильно выполниться.

Critical (50): этот уровень используется для вывода сведений об очень серьёзных
ошибках, наличие которых угрожает нормальному функционированию всего 
приложения. Если не исправить такую ошибку — это может привести к тому, 
что приложение прекратит работу.

filename - файл для логов.

filemode - режим работы с файлом.
По стандарту лучше использовать мод "a" или "r+", чтобы не перезаписывать
журнал.
"""

dp = Dispatcher()  # Диспетчер

"""
    Апдейт — любое событие: сообщение, редактирование сообщения, колбэк, 
инлайн-запрос, платёж, добавление бота в группу и т.д.

    Хэндлер — асинхронная функция, которая получает от диспетчера/роутера 
очередной апдейт и обрабатывает его.

    Роутер — объект, занимающийся получением апдейтов от Telegram с 
последующим выбором хэндлера для обработки принятого апдейта.

    Диспетчер - корневой роутер.

    Фильтр - условие для запуска хэндлера.
"""


async def main():
    dp.include_routers(router_1, router_unknow)
    await dp.start_polling(bot)  # Запуск процесса поллинга (ввода-вывода) новых апдейтов


if __name__ == "__main__":
    asyncio.run(main())
