import json
import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import requests

# === CONFIG ===
TOKEN = "8291438508:AAHgthyIsWwe1ASV-OW_MrH1_qtl7ECM0zk"
WEBHOOK_URL = "https://discord.com/api/webhooks/1486446590188196145/rGH5CIxK6ph3XxDPdP7P2iybT70jR77JjVVp7hkhmKIIyRBhq0ZK41A9WbfjEsoaRjbY"
APK_FILE_ID = "BQACAgIAAxkBAAOQacb5RJ6tIwtzuIryM_435oIajBwAAuSXAAJ4ejhKhpsumGAAAYs_OgQ"
USERS_FILE = "users.json"

KEYS = [
    "lunacy:VcuhIdib2CVt8eVZ6q7ErSxJhQLfzQr5FbQsBPVwgIDs",
    "lunacy:cfd69de8eb7d1c394041150a5cffa253r5FbQsBPr5FbQs",
    "lunacy:d30fd63cc3e79280a39bbe6ef6feed15d30fd63cc3e792",
]

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


# === DB ===
def load_users() -> dict:
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_users(data: dict):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_user(user_id: int) -> dict:
    users = load_users()
    return users.get(str(user_id), {"free_used": False, "key": None})


def set_user(user_id: int, data: dict):
    users = load_users()
    users[str(user_id)] = data
    save_users(users)


# === DISCORD ===
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
        requests.post(WEBHOOK_URL, json=data, timeout=5)
    except Exception:
        pass


# === KEYBOARD ===
def build_keyboard(hide_free: bool) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    if not hide_free:
        keyboard.add(InlineKeyboardButton("🎁 Получить бесплатно", callback_data="free"))
    keyboard.add(
        InlineKeyboardButton("📥 Install Lunacy", callback_data="download"),
        InlineKeyboardButton("📢 Подписаться на канал", url="https://t.me/Lunacy_Standoff"),
    )
    return keyboard


# === /start ===
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await send_to_discord(message.from_user)

    user_data = get_user(message.from_user.id)
    hide_free = user_data["free_used"]
    keyboard = build_keyboard(hide_free)

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
    )

    if hide_free and user_data.get("key"):
        text += f"\n🔑 <b>Ваш ключ:</b> <code>{user_data['key']}</code>"

    text += "\n\n👇 <b>Выберите действие ниже:</b>"

    await message.answer(text, reply_markup=keyboard)


# === CALLBACK: FREE ===
@dp.callback_query_handler(lambda c: c.data == "free")
async def free(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_data = get_user(user_id)

    if user_data["free_used"]:
        await callback_query.answer("Вы уже использовали бесплатный ключ.", show_alert=True)
        return

    # Assign key and mark as used
    assigned_key = random.choice(KEYS)
    user_data["free_used"] = True
    user_data["key"] = assigned_key
    set_user(user_id, user_data)

    await callback_query.message.answer(
        "⏳ Генерация ключа... Это занимает примерно 5 минут. После этого нажмите /start"
    )
    await callback_query.answer()


# === CALLBACK: DOWNLOAD ===
@dp.callback_query_handler(lambda c: c.data == "download")
async def download(callback_query: types.CallbackQuery):
    caption = (
        "📥 <b>Lunacy APK</b>\n\n"
        "🔥 Последняя версия\n"
        "⚡ Стабильная работа\n\n"
        "📋 <b>Инструкция по установке:</b>\n"
        "1️⃣ Скачайте APK файл на устройство\n"
        "2️⃣ Разрешите установку из неизвестных источников в настройках\n"
        "3️⃣ Откройте файл и нажмите «Установить»"
    )
    try:
        await bot.send_document(
            chat_id=callback_query.from_user.id,
            document=APK_FILE_ID,
            caption=caption,
        )
    except Exception as e:
        await callback_query.message.answer(f"❌ Ошибка при отправке файла: {e}")
    await callback_query.answer()


# === RUN ===
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
