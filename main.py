import asyncio
import logging
from tkinter.tix import Form
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

import analyse

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=)
# Диспетчер
dp = Dispatcher()


class Form(StatesGroup):
    mood = State()
    emotion = State()
    mode = State()


@dp.message(F.voice)
async def handle_voice(message: types.Voice):
    await bot.download(file=message.voice.file_id,
                       destination=f"E:\data\{message.from_user.id}.wav")


@dp.message(Command('start'))
async def start_questionnaire_process(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Привет! Я - Светик, как у тебя настроение, Хорошее или Плохое?')
    await state.set_state(Form.emotion)


@dp.message(F.Voice, Form.emotion)
async def capture_emotion(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Выбери одну из этих эмоций которая точнее всего описвыает твое состояние)')
    await state.set_state(Form.mode)


@dp.message(F.Voice, Form.mode)
async def capture_mode(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Хочешь расслабиться? Или может взбодриться? Выбери режим работы комнаты, '
                             'успокаивающий или энергичный')
    await state.set_state(Form.mood)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
