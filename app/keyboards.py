import logging
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Каталог')],
        [KeyboardButton(text='Стикеры')],  # Заменили "Недавние" на "Стикеры"
        [KeyboardButton(text='Помощь'), KeyboardButton(text='О нас')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню...'
)

catalog = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Лев Толстой', callback_data='ltolstoy')],
        [InlineKeyboardButton(text='Алексей Толстой', callback_data='atolstoy')],
        [InlineKeyboardButton(text='Ф.М.Достоевский', callback_data='fmdostoevsckiy')],
        [InlineKeyboardButton(text='М.А.Булгаков', callback_data='mabulgakov')]
    ]
)

logger.info("Клавиатуры успешно инициализированы")
