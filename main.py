import asyncio
import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, Voice
from aiogram.utils.chat_action import ChatActionSender
import speech_recognition as sr
import soundfile as sf
import os
from analyse import mood_detector, emotion_detector

r = sr.Recognizer()

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="inserttoken")
# Диспетчер
dp = Dispatcher()
questionnaire_router = Router()
dp.include_router(questionnaire_router)


class Form(StatesGroup):
    mood = State()
    emotion = State()
    mode = State()


async def handle_voice(message: types.Message):
    namefl = message.message_id
    voice = message.voice
    await bot.download(
        file=voice.file_id,
        destination=f"./audio/{namefl}.ogg"
    )
    data, samplerate = sf.read(f'./audio/{namefl}.ogg')
    sf.write(f'./audio/{namefl}.wav', data, samplerate)

    audio_file = sr.AudioFile(f'./audio/{namefl}.wav')
    with audio_file as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio, language='ru')
        except sr.UnknownValueError:
            text = "Не удалось распознать речь"

    os.remove(f'./audio/{namefl}.ogg')
    os.remove(f'./audio/{namefl}.wav')
    return text


@dp.message(Command('start'))
async def start_questionnaire_process(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Привет! Я - Светик, какое у тебя прошел день? Хорошо или Плохо?\n')
    await state.set_state(Form.emotion)


@questionnaire_router.message(Form.emotion, F.voice)
async def capture_emotion(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        text = await handle_voice(message)

        answ = mood_detector(text)
        if answ == 'good':
            await message.answer('Хорошее настроение это прекрасно! Я рад что у тебя все в порядке')
        elif answ == 'bad':
            await message.answer('Грустно, что у тебя плохое настроение, давай попробуем его улучшить!')

        await message.answer('Расскажи о своих эмоциях, опиши ту, которая точнее всего описывает твое состояние:\n'
                             'Экстаз, восхищение, изумление, ярость, отвращение, горе, ужас')
    await state.set_state(Form.mode)


@questionnaire_router.message(Form.mode, F.voice)
async def capture_mode(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        text = await handle_voice(message)
        emotion = emotion_detector(text)
        if emotion == 'mode1':
            await message.answer('Это очень хорошая эмоция, рад что ты ее испытываешь!')
        elif emotion == 'mode2':
            await message.answer('Жаль, что тебе приходится испытывать эту эмоцию, но я могу помочь тебе расслабиться!')

        await message.answer('Хочешь расслабиться? Или может взбодриться? Выбери режим работы комнаты: '
                             'успокаивающий или энергичный')
    await state.clear()



# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
