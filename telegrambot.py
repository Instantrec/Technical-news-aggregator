import logging
import os
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('INFO_TECH_NEWS_BOT_TOKEN'))
dp = Dispatcher(bot)

@dp.message_handler(commands='news')
async def echo(message: types.Message):
    with open('collected_data.txt', 'r') as f:
        news = f.readlines()

    news = ''.join(news)
    await message.answer(news) 

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

    
