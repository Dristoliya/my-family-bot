import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
# Используем новый официальный клиент Google Gen AI
from google import genai 

# ==================== НАСТРОЙКИ КЛЮЧЕЙ ====================
# 1. Твой токен от @BotFather (уже на месте)
TELEGRAM_TOKEN = "8965787272:AAEH0lZwfL-QBmwzqzIMx8MBEu6Z-U8u_4w"

# 2. Твой рабочий ключ от Gemini (уже на месте!)
GOOGLE_API_KEY = "AQ.Ab8RN6IrmJ5bdAlMYX0SIpl52V4LWB50zY7Vl9Rq-MFaqqo7UA"
# ==========================================================

# Настраиваем клиент ИИ и передаем ему ключ напрямую
ai_client = genai.Client(api_key=GOOGLE_API_KEY)

# Настраиваем Telegram-бота
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Инструкция для ИИ (Промпт) — заставляем его быть умным семейным штурманом
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
        # Переключились на актуальную модель gemini-3.6-flash, чтобы избежать ошибки 404
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
    # Сбрасываем вебхук от старых конструкторов и удаляем застрявшие сообщения
    await bot.delete_webhook(drop_pending_updates=True) 
    # Запускаем опрос сервера
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
