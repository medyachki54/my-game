import asyncio
import aiosqlite
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# 1. ЗАМЕНИ НА СВОЙ ТОКЕН
API_TOKEN = '8722317821:AAF0Yx9UyKFgoX0DJ3qThwwvSpob5e0GC9s'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def init_db():
    async with aiosqlite.connect("game.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER DEFAULT 0,
                income INTEGER DEFAULT 0,
                click_power INTEGER DEFAULT 1
            )
        """)
        await db.commit()

def main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Открыть игру (WebApp)", web_app=WebAppInfo(url="https://clonestars.space/clicker/"))],
        [InlineKeyboardButton(text="⚡️ Просто кликнуть", callback_data="click")],
        [InlineKeyboardButton(text="👤 Мой профиль", callback_data="me")]
    ])

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    async with aiosqlite.connect("game.db") as db:
        # Исправляем ошибку UNIQUE: используем OR IGNORE
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (message.from_user.id,))
        await db.commit()
    
    await message.answer("Добро пожаловать в игру! Выбирай режим:", reply_markup=main_kb())

@dp.callback_query(F.data == "click")
async def click_handler(callback: types.CallbackQuery):
    async with aiosqlite.connect("game.db") as db:
        await db.execute("UPDATE users SET balance = balance + click_power WHERE user_id = ?", (callback.from_user.id,))
        await db.commit()
        async with db.execute("SELECT balance FROM users WHERE user_id = ?", (callback.from_user.id,)) as cursor:
            row = await cursor.fetchone()
    
    await callback.answer(f"Клик! Баланс: {row[0]} $")

async def main():
    await init_db()
    print("Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Ошибка при запуске: {e}")

