from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

class PrivatChat(BoundFilter):
    key = 'private'

    def __init__(self, private):
        self.private = private

    async def check(self, message: types.Message):
        chat = await message.chat.type
        return chat
