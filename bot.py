import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


# ==============================
# CONFIGURATION
# ==============================

BOT_TOKEN = "8406688505:AAGkmKI4rUagmq7n9wlV30ZodOAWecZZRAo"
OWNER_ID = 8547982063


# ==============================
# LOGGING
# ==============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# ==============================
# BOT SETUP
# ==============================

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()


# ==============================
# START COMMAND
# ==============================

@dp.message(CommandStart())
async def start_cmd(message: types.Message):

    user = message.from_user
    name = user.first_name if user else "User"

    await message.answer(
        f"👋 <b>আসসালামু আলাইকুম, {name}!</b>\n\n"
        "🎉 <b>অভিনন্দন!</b>\n"
        "আপনার Telegram Bot সফলভাবে চালু হয়েছে। 🚀\n\n"
        "🟢 <b>Status:</b> Online\n"
        "⚡ <b>System:</b> Aiogram\n"
        "☁️ <b>Server:</b> Render\n\n"
        "💡 বট এখন কাজ করার জন্য প্রস্তুত।"
    )


# ==============================
# BASIC MESSAGE HANDLER
# ==============================

@dp.message()
async def message_handler(message: types.Message):

    await message.answer(
        "🤖 আপনার মেসেজ পেয়েছি!\n\n"
        "ব্যবহার শুরু করতে /start লিখুন।"
    )


# ==============================
# MAIN FUNCTION
# ==============================

async def main():

    logging.info("Starting Telegram Bot...")

    try:
        # Remove old webhook
        await bot.delete_webhook(drop_pending_updates=True)

        logging.info("Bot is running successfully!")

        # Start polling
        await dp.start_polling(bot)

    except Exception as error:
        logging.exception(f"Bot stopped due to error: {error}")

    finally:
        await bot.session.close()
        logging.info("Bot session closed.")


# ==============================
# RUN BOT
# ==============================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped manually.")
