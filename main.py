from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import requests

# === НАСТРОЙКИ ===
TOKEN = "ТВОЙ_ТОКЕН"
WEBHOOK_URL = "ТВОЙ_DISCORD_WEBHOOK"

APK_FILE_ID = "YOUR_FILE_ID_HERE"  # <-- ВСТАВЬ СЮДА file_id

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# === ОТПРАВКА В DISCORD ===
async def send_to_discord(user):
    data = {
        "content": (
            f"🚀 Новый пользователь!\n\n"
            f"👤 Username: @{user.username}\n"
            f"🆔 ID: {user.id}\n"
            f"📛 Имя: {user.full_name}"
        )
    }
    try:
        requests.post(WEBHOOK_URL, json=data)
    except:
        pass

# === ПОЛУЧЕНИЕ FILE_ID (временно) ===
@dp.message_handler(content_types=['document'])
async def get_file_id(message: types.Message):
    file_id = message.document.file_id
    await message.reply(f"FILE_ID:\n{file_id}")

# === START ===
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await send_to_discord(message.from_user)

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🎁 Получить бесплатно", callback_data="free"),
        InlineKeyboardButton("📥 Скачать APK", callback_data="download"),
        InlineKeyboardButton("📢 Подписаться на канал", url="https://t.me/Lunacy_Standoff")
    )

    text = (
        "👋 <b>Добро пожаловать в Lunacy Shop</b>\n\n"

        "💎 <b>Lunacy для Standoff 2 — мощный и актуальный чит</b>\n\n"

        "⚡ <b>Основные преимущества:</b>\n"
        "— Стабильная и быстрая работа без вылетов\n"
        "— Полностью актуальная версия — 0.37.1\n"
        "— Удобный и понятный интерфейс\n"
        "— Регулярные обновления\n\n"

        "🔥 <b>Функционал:</b>\n"
        "— Skinchanger (работают все скины)\n"
        "— Полный доступ ко всем функциям\n"
        "— Оптимизация под слабые и мощные устройства\n"
        "— Быстрый запуск без лишних настроек\n\n"

        "🛡 <b>Надёжность:</b>\n"
        "— Проверенная сборка\n"
        "— Минимальный риск\n"
        "— Поддержка при покупке\n\n"

        "📱 <i>После покупки вы можете выбрать версию под своё устройство: Android, Windows или iPhone</i>\n\n"

        "💰 <b>Цена:</b> 149₽\n\n"
        "🛒 <b>Покупка:</b> @frokzer\n\n"

        "📩 <i>После покупки вы получите доступ и инструкцию</i>\n"
        
        "👇 <b>Выберите действие ниже:</b>"
    )

    await message.answer(text, reply_markup=keyboard)

# === CALLBACK: FREE ===
@dp.callback_query_handler(lambda c: c.data == "free")
async def free(callback_query: types.CallbackQuery):
    alert_text = (
        "⏳ Пока недоступно!\n\n"
        "Эта функция откроется, как только в нашем канале наберется 15 подписчиков. "
        "Подписывайся, чтобы не пропустить!"
    )
    await callback_query.answer(alert_text, show_alert=True)

# === CALLBACK: DOWNLOAD APK ===
@dp.callback_query_handler(lambda c: c.data == "download")
async def download(callback_query: types.CallbackQuery):
    await bot.send_document(
        chat_id=callback_query.from_user.id,
        document=APK_FILE_ID,
        caption="📥 Вот твой APK файл"
    )
    await callback_query.answer()

# === ЗАПУСК ===
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
