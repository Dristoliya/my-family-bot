import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import google.generativeai as genai

# Твой токен от @BotFather
TELEGRAM_TOKEN = "8965787272:AAEH0lZwfL-QBmwzqzIMx8MBEu6Z-U8u_4w"

# Настраиваем ИИ. Он сам заберет ключ из настроек Railway
genai.configure()

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

AI_PROMPT = (
    "Ты — продвинутый и заботливый ИИ-ассистент в семейном Telegram-боте дальнобойщика. "
    "Твоя задача — общаться с женой водителя тепло, вежливо и с заботой. "
    "Отвечай живым языком, используй смайлики."
)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! 👋\nИИ-Штурман запущен и готов к работе!")

@dp.message()
async def handle_ai_message(message: types.Message):
    full_request = f"{AI_PROMPT}\n\nПользователь пишет: {message.text}"
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(full_request)
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"⚠️ Ошибка ИИ: {e}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True) 
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
