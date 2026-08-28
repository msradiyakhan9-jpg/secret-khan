import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

BOT_TOKEN = os.getenv("8406688505:AAGkmKI4rUagmq7n9wlV30ZodOAWecZZRAo")
OWNER_ID = os.getenv("8547982063")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("অভিনন্দন! আপনার টেলিগ্রাম বটটি Render-এ সফলভাবে চালু হয়েছে! 🚀")

async def main():
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
