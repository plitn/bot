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


# Проверка на существование в бд, регистрация (просто имя)
@dp.message_handler(commands='reg')
async def get_text_messages(message):
    if db.user_exists(message.from_user.username):
        await bot.send_message(message.from_user.id, 'Ты уже зарегистрирован!')
    else:
        await Form.name.set()
        await bot.send_message(message.from_user.id, 'Как тебя зовут?')


# Регистрируем имя
@dp.message_handler(state=Form.name)
async def process_name(message: types.message, state: FSMContext):
    name = message.text
    await state.finish()
    print(message.from_user.username)
    db.add_user(str(message.from_user.username), name)
    await bot.send_message(message.from_user.id, 'Ты зарегистрирован!')


# Обработка обращения к менюшке, потом сделаем
@dp.message_handler(commands=['menu'])
async def show_menu(message: types.message):
    await message.reply('меню')


# Обработка обращения к профилю, потом сделаем
@dp.message_handler(commands=['profile'])
async def show_profile(message: types.message):
    await bot.send_message(message.from_user.id, 'Твой профиль:')
    await bot.send_message(message.from_user.id, db.get_name(message.from_user.username) + '\nВсего очков: ' + str(
        db.get_points(message.from_user.username)))


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown())
