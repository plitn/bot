from db import Database
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
import markup


TOKEN = '5250676031:AAH5cZ7YFzDdgyBS8ijK0l9AD1FKEVVTbrg'
bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database('hse_curator.db')

current_question_id = 0


class Form(StatesGroup):
    answer = State()


@dp.message_handler(commands='start')
async def start(message):
    await bot.send_message(message.from_user.id, 'Привет! Увидел твой профиль в группе для абитуриентов, не ответишь '
                                                 'мне на пару вопросов про вышку? Собираюсь поступать к вам, '
                                                 'но пока что вообще не понимаю, что там да как(((')
    if not db.user_exists(str(message.from_user.username)):
        db.add_user(str(message.from_user.username))
    await Form.answer.set()


# Checking if answer is correct
def is_answer_correct(ans, user_id):
    return ans == db.get_correct_answer_id(db.get_current_question_id(user_id))


# Gets next questions and answers
async def next_question(message):
    if db.get_current_question_id(message.from_user.username) <= db.check_max_id():
        await bot.send_message(message.from_user.id, db.get_question_text(message.from_user.username))
        if db.get_number_of_variants(db.get_current_question_id(message.from_user.username)) == 4:
            await bot.send_message(message.from_user.id,
                                   db.get_variants(db.get_current_question_id(message.from_user.username)),
                                   reply_markup=markup.inline_answers4)
        elif db.get_number_of_variants(db.get_current_question_id(message.from_user.username)) == 3:
            await bot.send_message(message.from_user.id,
                                   db.get_variants(db.get_current_question_id(message.from_user.username)),
                                   reply_markup=markup.inline_answers3)
        elif db.get_number_of_variants(db.get_current_question_id(message.from_user.username)) == 2:
            await bot.send_message(message.from_user.id,
                                   db.get_variants(db.get_current_question_id(message.from_user.username)),
                                   reply_markup=markup.inline_answers2)
        elif db.get_number_of_variants(db.get_current_question_id(message.from_user.username)) == 0:
            await Form.answer.set()
    else:
        await print_goodbye(message)


# Goodbye at the end of questions
async def print_goodbye(message):
    await bot.send_message(message.from_user.id,
                           'Спасибо большое за ответы на мои непростые вопросы! Надеюсь, в скором времени увидимся с '
                           'тобой уже в стенах вышки!', reply_markup=markup.inline_restart)
    await bot.send_message(message.from_user.id, 'Вот тебе небольшой подарочек за прохождение вопросов \n'
                                                 '<a href="https://t.me/addstickers/HSE_MENTORS">Тык</a>',
                           parse_mode='HTML')


# Waiting for user's text answer
@dp.message_handler(state=Form.answer)
async def something_answered(message, state: FSMContext):
    db.change_current_question_id(message.from_user.username)
    await state.finish()
    await next_question(message)


# Reply for wrong answer
async def show_reply(message):
    await bot.send_message(message.from_user.id,
                           db.get_answer_reply(db.get_current_question_id(message.from_user.username)))


@dp.callback_query_handler(text='restart_btn')
async def restart_pressed(message):
    db.restart_questions(message.from_user.username)
    await start(message)


# 4 methods for buttons being pressed
@dp.callback_query_handler(text='btn1')
async def btn1_pressed(message):
    if not is_answer_correct(1, message.from_user.username) and db.get_number_of_variants(db.get_current_question_id(message.from_user.username)) != 0:
        await show_reply(message)
        await next_question(message)
    else:
        db.change_current_question_id(message.from_user.username)
        await next_question(message)


@dp.callback_query_handler(text='btn2')
async def btn2_pressed(message):
    if not is_answer_correct(2, message.from_user.username) and db.get_number_of_variants(db.get_current_question_id(message.from_user.username)) != 0:
        await show_reply(message)
        await next_question(message)
    else:
        db.change_current_question_id(message.from_user.username)
        await next_question(message)


@dp.callback_query_handler(text='btn3')
async def btn3_pressed(message):
    if not is_answer_correct(3, message.from_user.username) and db.get_number_of_variants(db.get_current_question_id(message.from_user.username)) != 0:
        await show_reply(message)
        await next_question(message)
    else:
        db.change_current_question_id(message.from_user.username)
        await next_question(message)


@dp.callback_query_handler(text='btn4')
async def btn4_pressed(message):
    if not is_answer_correct(4, message.from_user.username) and db.get_number_of_variants(db.get_current_question_id(message.from_user.username)) != 0:
        await show_reply(message)
        await next_question(message)
    else:
        db.change_current_question_id(message.from_user.username)
        await next_question(message)


# Not used. why?
async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp)
