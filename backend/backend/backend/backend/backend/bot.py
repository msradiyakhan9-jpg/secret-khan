import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from database import SessionLocal, init_database
from models import User
from admin_panel import OwnerControlCenter
from config import settings

bot = Bot(token=settings.bot_token)
dp = Dispatcher()
router = Router()

def get_main_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📸 Photos"), KeyboardButton(text="🎬 Videos")],
        [KeyboardButton(text="🎙️ Voice"), KeyboardButton(text="📄 Documents")],
        [KeyboardButton(text="👑 OWNER CONTROL CENTER")]
    ], resize_keyboard=True)

@router.message(Command("start"))
async def start_cmd(message: Message):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == message.from_user.id).first()
        if not user:
            role = "OWNER" if message.from_user.id == settings.owner_id else "USER"
            user = User(id=message.from_user.id, username=message.from_user.username, role=role)
            db.add(user)
            db.commit()

        m_mode = OwnerControlCenter.get_setting(db, "maintenance_mode", "false")
        if m_mode == "true" and message.from_user.id != settings.owner_id:
            await message.answer("🔧 **সিস্টেম মেইনটেন্যান্স চলছে।** কিছুক্ষণ পর চেষ্টা করুন।")
            return

        await message.answer("🔒 **প্রাইভেট ভল্ট বটে স্বাগতম!**", reply_markup=get_main_keyboard())
    finally:
        db.close()

@router.message(F.text == "👑 OWNER CONTROL CENTER")
async def owner_panel_menu(message: Message):
    if message.from_user.id != settings.owner_id:
        return
        
    db = SessionLocal()
    try:
        m_mode = OwnerControlCenter.get_setting(db, "maintenance_mode", "false")
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"🛠️ Maintenance: {'🔴 ON' if m_mode=='true' else '🟢 OFF'}", callback_data="toggle_m_mode")],
            [InlineKeyboardButton(text="📢 Broadcast Message", callback_data="owner_broadcast")]
        ])
        await message.answer("👑 **OWNER CONTROL CENTER**\nকোড না পরিবর্তন করেই সব নিয়ন্ত্রণ করুন:", reply_markup=kb)
    finally:
        db.close()

@router.callback_query(F.data == "toggle_m_mode")
async def toggle_maintenance(callback: CallbackQuery):
    if callback.from_user.id != settings.owner_id:
        return
    db = SessionLocal()
    try:
        curr = OwnerControlCenter.get_setting(db, "maintenance_mode", "false")
        new_val = "false" if curr == "true" else "true"
        OwnerControlCenter.update_setting(db, "maintenance_mode", new_val)
        await callback.answer(f"Maintenance status: {new_val.upper()}")
        await owner_panel_menu(callback.message)
    finally:
        db.close()

async def main():
    init_database()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
