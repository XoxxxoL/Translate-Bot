from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp

@dp.message_handler()
async def us(message: types.Message):
    print(message)
