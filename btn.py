from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


menu_btn = InlineKeyboardMarkup(row_width=1)
menu_btn.add(
    InlineKeyboardButton(text='Raccil', callback_data="raccil"),
)

