from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_btn1 = InlineKeyboardButton('1️⃣', callback_data='btn1')
inline_btn2 = InlineKeyboardButton('2️⃣', callback_data='btn2')
inline_btn3 = InlineKeyboardButton('3️⃣', callback_data='btn3')
inline_btn4 = InlineKeyboardButton('4️⃣', callback_data='btn4')

# Keyboard for 4 answers
inline_answers4 = InlineKeyboardMarkup(row_width=2)
inline_answers4.add(inline_btn1, inline_btn2, inline_btn3, inline_btn4)

# Keyboard for 3 answers
inline_answers3 = InlineKeyboardMarkup(row_width=1)
inline_answers3.add(inline_btn1, inline_btn2, inline_btn3)

# Keyboard for 2 answers
inline_answers2 = InlineKeyboardMarkup(row_width=2)
inline_answers2.add(inline_btn1, inline_btn2)
