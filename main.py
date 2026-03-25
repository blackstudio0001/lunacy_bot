from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

TOKEN = "8291438508:AAHgthyIsWwe1ASV-OW_MrH1_qtl7ECM0zk"

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🎁 Получить бесплатно", callback_data="free"),
        InlineKeyboardButton("📢 Подписаться на канал", url="https://t.me/Lunacy_Standoff")
    )

    text = (
        "👋 <b>Здравствуйте! Добро пожаловать в наш SHOP.</b>\n\n"
        "💎 <b>Цена Lunacy:</b> 149₽\n\n"
        "<i>Выберите нужное действие ниже:</i>"
    )
    await message.answer(text, reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "free")
async def free(callback_query: types.CallbackQuery):
    alert_text = (
        "⏳ Пока недоступно!\n\n"
        "Эта функция откроется, как только в нашем канале наберется 15 подписчиков. "
        "Подписывайся, чтобы не пропустить!"
    )
    await callback_query.answer(alert_text, show_alert=True)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)