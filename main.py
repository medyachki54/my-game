import asyncio
import aiosqlite
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# --- НАСТРОЙКИ ---
API_TOKEN = '8722317821:AAF0Yx9UyKFgoX0DJ3qThwwvSpob5e0GC9s' 

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- БАЗА ДАННЫХ ---
async def init_db():
    async with aiosqlite.connect("game.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                user_name TEXT,
                balance INTEGER DEFAULT 0,
                income INTEGER DEFAULT 0,
                click_power INTEGER DEFAULT 1
            )
        """)
        await db.commit()

# --- ЛОГИКА ДОХОДА ---
async def income_scheduler():
    while True:
        await asyncio.sleep(60) # Начисляем раз в минуту
        async with aiosqlite.connect("game.db") as db:
            # Начисляем доход (делим на 60, так как доход указан за час)
            await db.execute("UPDATE users SET balance = balance + (income / 60) WHERE income > 0")
            await db.commit()

def get_status(balance):
    if balance < 100: return "Новичок 👶"
    if balance < 5000: return "Фрилансер ⚡️"
    if balance < 50000: return "Техлид 👨‍🏫"
    return "IT-Миллиардер 👑"

# --- КЛАВИАТУРЫ ---
def main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 ИГРАТЬ (Mini App)", web_app=WebAppInfo(url="https://clonestars.space/clicker/"))],
        [InlineKeyboardButton(text="👤 Профиль", callback_data="me"), InlineKeyboardButton(text="🛒 Магазин", callback_data="shop")],
        [InlineKeyboardButton(text="🏆 Топ игроков", callback_data="leaderboard")]
    ])

def shop_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⌨️ Мышка (+2 к клику) — 50$", callback_data="buy_click")],
        [InlineKeyboardButton(text="🖥 Сервер (+60$/час) — 200$", callback_data="buy_income")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="me")]
    ])

# --- ОБРАБОТЧИКИ ---

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    async with aiosqlite.connect("game.db") as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id, user_name) VALUES (?, ?)", 
                         (message.from_user.id, message.from_user.first_name))
        await db.commit()
    await message.answer(f"Привет! Твоя IT-империя начинается здесь.", reply_markup=main_kb())

@dp.callback_query(F.data == "me")
async def show_profile(callback: types.CallbackQuery):
    async with aiosqlite.connect("game.db") as db:
        async with db.execute("SELECT balance, income, click_power FROM users WHERE user_id = ?", (callback.from_user.id,)) as cursor:
            row = await cursor.fetchone()
    
    status = get_status(row[0])
    text = (
        f"👤 **Игрок:** {callback.from_user.first_name}\n"
        f"🏅 **Статус:** {status}\n\n"
        f"💰 Баланс: **{int(row[0])} $**\n"
        f"📈 Доход: **{row[1]} $/час**\n"
        f"⚡️ Сила клика: **{row[2]} $**"
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=main_kb())

@dp.callback_query(F.data == "shop")
async def open_shop(callback: types.CallbackQuery):
    await callback.message.edit_text("🛒 **Магазин**\nУлучшай оборудование, чтобы зарабатывать больше!", 
                                     parse_mode="Markdown", reply_markup=shop_kb())

@dp.callback_query(F.data.startswith("buy_"))
async def buy_item(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    async with aiosqlite.connect("game.db") as db:
        async with db.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)) as cursor:
            balance = (await cursor.fetchone())[0]
        
        if callback.data == "buy_click" and balance >= 50:
            await db.execute("UPDATE users SET balance = balance - 50, click_power = click_power + 2 WHERE user_id = ?", (user_id,))
            res = "Куплено! Клик стал сильнее 💪"
        elif callback.data == "buy_income" and balance >= 200:
            await db.execute("UPDATE users SET balance = balance - 200, income = income + 60 WHERE user_id = ?", (user_id,))
            res = "Куплено! Доход вырос на 60$/час 📈"
        else:
            res = "Недостаточно средств! ❌"
        await db.commit()
    await callback.answer(res)

@dp.callback_query(F.data == "leaderboard")
async def show_leaderboard(callback: types.CallbackQuery):
    async with aiosqlite.connect("game.db") as db:
        async with db.execute("SELECT user_name, balance FROM users ORDER BY balance DESC LIMIT 5") as cursor:
            rows = await cursor.fetchall()
    
    text = "🏆 **ТОП-5 МАГНАТОВ**\n\n"
    for i, row in enumerate(rows, 1):
        text += f"{i}. {row[0]} — {int(row[1])}$\n"
    await callback.message.edit_text(text, reply_markup=main_kb())

# --- ЗАПУСК ---
async def main():
    await init_db()
    asyncio.create_task(income_scheduler()) # Запуск фонового дохода
    print(">>> Бот работает!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

