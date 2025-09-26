# bot.py
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from alibabacloud_wanxiang20230601.client import Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_wanxiang20230601 import models as wanxiang_models

# === Настройки ===
BOT_TOKEN = "8483804350:AAENdRj3dslq8ihpo-v40W8RQaeXOxshpm8"
ALIBABA_KEY = os.getenv("LTAI5tJxHXdiVL5SURv4Dt7b")
ALIBABA_SECRET = os.getenv("CAWMfE8KMfX8CnnALzmII89Hdxtend")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_wanxiang_client():
    config = open_api_models.Config(
        access_key_id=LTAI5tJxHXdiVL5SURv4Dt7b,
        access_key_secret=CAWMfE8KMfX8CnnALzmII89Hdxtend,
        region_id="ap-southeast-1"  # Сингапур — лучше доступ из РФ
    )
    return Client(config)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "📸 Привет! Присылай рендер из C4D/Blender и напиши команду:\n\n"
        "Примеры:\n"
        "• `winter, snow, photorealistic`\n"
        "• `summer sunset, wet asphalt`\n"
        "• `cyberpunk city, neon lights`\n\n"
        "⚡ Результат — за 10 секунд!"
    )

@dp.message(types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]  # берем самое большое изображение
    file = await bot.get_file(photo.file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"
    
    prompt = message.caption or "photorealistic, 8k, cinematic lighting"
    await message.answer("🎨 Обрабатываю... (~10 сек)")

    try:
        client = get_wanxiang_client()
        request = wanxiang_models.ImageRefineRequest(
            input_image_url=file_url,
            prompt=prompt,
            style="photographic"
        )
        response = client.image_refine(request)
        result_url = response.body.data.url
        await message.answer_photo(photo=result_url, caption="✨ Готово!")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")

# === Запуск ===
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
