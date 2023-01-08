import logging
import uuid
from io import BytesIO

from aiogram import Dispatcher, Bot, types
from aiogram.utils import executor
from configs import TOKEN, ENV
from logic import save_photo, save_chat_id

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Hello it\'s bot for sending images by schedule')


@dp.channel_post_handler(text='/chain')
async def channel_chain(message: types.Message):
    await save_chat_id(str(message.chat.id))
    logger.info(f'{message.chat.id} saved')
    await message.answer('Channel chained')


@dp.message_handler(content_types=['photo'])
async def send_photo(message):
    file_name = str(uuid.uuid4())
    image = BytesIO()
    photo = await message.photo[-1].download(destination_file=image)
    await save_photo(file_name, photo)
    await message.answer('Photo added')


if __name__ == '__main__':
    if ENV == 'local':
        executor.start_polling(dp, skip_updates=True)
