import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from google import genai 

# Берем API-ключ ИИ из настроек сервера Render
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")

# Настраиваем клиент ИИ автоматически
ai_client = genai.Client(api_key=GOOGLE_API_KEY)

# ==================== ТОКЕН TELEGRAM ====================
TELEGRAM_TOKEN = "8965787272:AAEH0lZwfL-QBmwzqzIMx8MBEu6Z-U8u_4w"
# ========================================================

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Инструкция для ИИ (Промпт)
AI_PROMPT = (
    "Ты — продвинутый и заботливый ИИ-ассистент в семейном Telegram-боте дальнобойщика. "
    "Твоя задача — общаться с женой водителя тепло, вежливо и с заботой. "
    "Ты должен анализировать её сообщения. Если она пишет важные даты (например, свой отпуск, "
    "праздники или дела), или если муж передает свой график рейсов — ты должен это запоминать "
    "и учитывать в ответах. Отвечай живым языком, используй смайлики."
)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! 👋\n"
        "Я твой новый грандиозный ИИ-Штурман на Python. "
        "Напиши мне что угодно — я отправлю это нейросети, и она сама подумает над ответом!"
    )

@dp.message()
async def handle_ai_message(message: types.Message):
    full_request = f"{AI_PROMPT}\n\nПользователь пишет: {message.text}"
    
    try:
        # Используем рабочую модель gemini-3.6-flash
        response = ai_client.models.generate_content(
            model='gemini-3.6-flash',
            contents=full_request,
        )
        await message.answer(response.text)
    except Exception as e:
        print(f"Ошибка ИИ: {e}")
        await message.answer("Ой, ИИ немного задумался. Проверь ключи настройки в коде!")

async def main():
    print("ИИ-Бот успешно запущен и готов думать!")
    await bot.delete_webhook(drop_pending_updates=True) 
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
