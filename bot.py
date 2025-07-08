import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

def get_instagram_media_url(insta_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get("https://saveinsta.app/en/download-instagram", headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find("input", {"id": "token"})["value"]
    data = {"q": insta_url, "t": "media", "lang": "en", "token": token}
    response = requests.post("https://saveinsta.app/action.php", headers=headers, data=data)
    soup2 = BeautifulSoup(response.text, "html.parser")
    link = soup2.find("a", {"target": "_blank"})["href"]
    return link

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Instagram linkini yuboring – men uni yuklab beraman.")

@dp.message_handler()
async def handle_message(message: types.Message):
    if "instagram.com" in message.text:
        await message.reply("⏬ Yuklanmoqda...")
        try:
            url = get_instagram_media_url(message.text)
            if url.endswith(".mp4"):
                await message.reply_video(video=url)
            else:
                await message.reply_photo(photo=url)
        except:
            await message.reply("❌ Yuklab bo‘lmadi. Iltimos, havolani tekshirib yuboring.")
    else:
        await message.reply("Instagram post linkini yuboring.")

if __name__ == "__main__":
    executor.start_polling(dp)
