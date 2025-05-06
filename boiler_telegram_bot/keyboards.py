from aiogram.utils.keyboard import ReplyKeyboardBuilder


def repair_bot_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='🏪 Перезапустить бота')

    keyboard_builder.adjust(2)

    return keyboard_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )