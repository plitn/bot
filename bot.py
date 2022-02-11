
from db import Database
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

TOKEN = '5250676031:AAH5cZ7YFzDdgyBS8ijK0l9AD1FKEVVTbrg'
bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database('hse_curator.db')

name = ''
age = -1

class Form(StatesGroup):
    name = State()

@dp.message_handler(commands='reg')
async def get_text_messages(message):
    if db.user_exitst(message.from_user.username):
        await bot.send_message(message.from_user.id, 'Ты уже зарегистрирован!')
    else:
        await get_name(message)
        #рега

@dp.message_handler()
async def get_name(message: types.message):
    await Form.name.set()
    await bot.send_message(message.from_user.id, 'Как тебя зовут?')

@dp.message_handler(state= Form.name)
async def process_name(message: types.message, state:FSMContext):
    name = message.text
    await state.finish()
    db.add_user(message.from_user.username, name)
    await bot.send_message(message.from_user.id, 'Ты зарегистрирован!')

@dp.message_handler(commands=['menu'])
async def show_menu(message: types.message):
    await message.reply('меню')

@dp.message_handler(commands=['profile'])
async def show_profile(message: types.message):
    await bot.send_message(message.from_user.id, 'твой профиль')

if __name__ == '__main__':
    executor.start_polling(dp)
