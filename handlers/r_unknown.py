from aiogram import Router, F
from aiogram.types import Message

router_unknow = Router()


@router_unknow.message(F.text)
async def message_with_text(message: Message):
    await message.answer("Допустим, что я вас понял!")


@router_unknow.message(F.sticker)
async def message_with_sticker(message: Message):
    await message.answer("Прикольный стикер...!")


@router_unknow.message(F.animation)
async def message_with_gif(message: Message):
    await message.answer("Мы что, в 2007?")


