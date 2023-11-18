import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from database import * 
from untils import *
from btn import *
from state import * 



import os
import untils
import state

BOT_TOKEN = "6502882014:AAE31XBkaUL1HrUh4E1Wb7VwmbiGXDdLGQ8"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

Admins = [1112362354]   



async def command_menu(dp: Dispatcher):
  await dp.bot.set_my_commands(
    [
      types.BotCommand('start', 'Ishga tushirish'),
      types.BotCommand('admin', 'Adminlar'),
    ]
  )
  await create_tables()

@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
  await add_user(message.from_user.id)
  await message.answer("Salom birodar")


############### Admin #############################

@dp.message_handler(commands=['admin'])
async def admin_handler(message: types.Message):
    if message.from_user.id in Admins:
      users = await  get_all_users()
      await message.answer(f"Bot azolar soni: {users}", reply_markup=menu_btn)

      await AdminStates.mailing.set()


@dp.message_handler(commands=['send'])
async def send_handler(message: types.Message):
  if message.from_user.id in Admins:
    await message.answer("Xabarni yuboring:")

    await AdminStates.mailing.set()


@dp.message_handler(content_types=['text','photo','animation','video','voice','audio'], state=AdminStates.mailing)
async def mailing_state(message: types.Message,state: FSMContext):
  text = message.text
  context = message.content_type
  users = await get_all_id()
  
  await state.finish()

  for user in users:
    if context == 'text':
      await bot.send_message(chat_id=user[0], text=text)
    elif context == 'photo':
      await bot.send_photo(chat_id=user[0], photo=message.photo[-1].file_id)
    elif context == 'animation':
      await bot.send_animation(chat_id=user[0], animation=message.animation.file_id)
    elif context == 'audio':
      await bot.send_audio(chat_id=user[0], audio=message.audio.file_id)
    elif context == 'voice':
      await bot.send_voice(chat_id=user[0], voice=message.voice.file_id)
    elif context == 'video':
      await bot.send_video(chat_id=user[0], video=message.video.file_id)

@dp.message_handler(content_types=['text'])
async def get_vidio_url_handler(message: types.Message):
  text = message.text

  if text.startswith("https://youtube.com" or text.startswith("https://youtu.be")) or text.startswith("https://www.youtube.com"):
    wait_wsg = await message.answer("⏳")
    video = await download_video_by_url(text, message.from_user.id)
    await wait_wsg.delete()

    if video == 1:
      await message.answer("Videoda tortish xatolik")
    elif video:
      await message.answer_video(types.InputFile(video))
    
      os.remove(video)
    else:
      await message.answer("Video 50 mb dan katta")




if __name__ == "__main__":
  executor.start_polling(dp, on_startup=command_menu)