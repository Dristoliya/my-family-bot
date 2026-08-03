import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import google.generativeai as genai

# ==================== НАСТРОЙКИ ТЕЛЕГРАМ ====================
TELEGRAM_TOKEN = "8965787272:AAEH0lZwfL-QBmwzqzIMx8MBEu6Z-U8u_4w"
# ============================================================

# Подключаем ИИ. Ключ автоматически берётся из переменной GOOGLE_API_KEY в Railway
genai.configure()

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Наша большая инструкция для ИИ
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
        # Используем актуальную и доступную для новых аккаунтов модель gemini-2.0-flash
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(full_request)
        await message.answer(response.text)
    except Exception as e:
        print(f"Ошибка ИИ: {e}")
        await message.answer(f"⚠️ Ошибка ИИ: {e}")

async def main():
    print("ИИ-Бот успешно запущен и готов думать!")
    await bot.delete_webhook(drop_pending_updates=True) 
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
