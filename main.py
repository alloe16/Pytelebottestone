from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from random import randint
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup,State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from time import sleep
from aiogram.utils import executor
import requests



# 5146993587:AAH90UV-KL8JyEtYRmZeusJrbyi40i9XTS4
token = '5146993587:AAH90UV-KL8JyEtYRmZeusJrbyi40i9XTS4'
bot = Bot(token=token)
dp = Dispatcher(bot,storage=MemoryStorage())

@dp.message_handler(commands='start')
async def fnc_start(messange: types.Message):
    await messange.answer('Hello')

@dp.message_handler(content_types=['photo'])
async def get_photo(messange: types.Message):
    await messange.photo[-1].download()

@dp.message_handler(commands='time')
async def cmd_awsd(messange:types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1='Кушаю'
    btn2='Поднимаюсь с кровати'
    btn3='Укладываюсь спать'
    keyboard.add(btn1)
    keyboard.add(btn2)
    keyboard.add(btn3)
    await messange.answer('Пожелания',reply_markup=keyboard)



@dp.message_handler(Text(equals='Кушаю'))
async def pupit_reply(messange:types.Message):
    await messange.reply('Приятного аппетита!',reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(Text(equals='Поднимаюсь с кровати'))
async def eat_reply(messange:types.Message):
    await messange.reply('Доброго утра и самого лучшего дня)',reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(Text(equals='Укладываюсь спать'))
async def sweet_reply(messange: types.Message):
    await messange.reply('Сладких снов,мое солнышко)', reply_markup=types.ReplyKeyboardRemove())

#@dp.message_handler(commands='rnd')
#async def cmn_rnd(message:types.Message):
#    keyboard = types.InlineKeyboardMarkup()
#    btn_one=types.InlineKeyboardButton(text='Get random int!' , callback_data='rnd_data')
#    keyboard.add(btn_one)
#    await message.answer('Click here',reply_markup=keyboard)


#@dp.callback_query_handler(text='rnd_data')
#async def send_randomint(call:types.CallbackQuery):
 #   await call.answer(str ( randint(1,100) )  )


@dp.message_handler(commands='makemecool1')
async def cmd_mmc1(messange:types.Message):
    await messange.answer('Привет, солнышко \U0001F498	')

@dp.message_handler(commands='makemecool2')
async def cmd_mmc2(messange:types.Message):
    await messange.answer('Желаю самого лучшего и продуктивного дня!')
@dp.message_handler(commands='makemecool3')
async def cmd_mmc3(messange:types.Message):
    user_id = messange.from_user.id
    await bot.send_sticker(user_id,'CAACAgIAAxkBAAEEMrBiNFUBTwFm93cGQSMc65yKHMzWeQACDAADwDZPE-LPI__Cd5-8IwQ')

avaible_messange=['люблю','целую','обнимаю']
avaible_size=['сильно','очень сильно','супер сильно']

class Orderlove(StatesGroup):
    waiting_for_messange=State()
    waiting_for_size=State()

async def lovestart(msg:types.Message):
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in avaible_messange:
        kb.add(name)

        await msg.answer('Выбери действие ',reply_markup=kb)
        await Orderlove.waiting_for_messange.set()

async def lovechoise(msg:types.Message,state:FSMContext):
    if msg.text.lower() not in avaible_messange:
        await msg.answer('Нужно сделать выбор из списка')
        return
    await state.update_data(love_choise=msg.text.lower())
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in avaible_size:
        kb.add(name)
    await Orderlove.next()
    await msg.answer('Выбери размер)',reply_markup=kb)

async def love_size_choise(msg:types.Message,state:FSMContext):
    if msg.text.lower() not in avaible_size:
        await msg.answer('Нужно выбрать размер из списка')
        return
    user_data = await state.get_data()
    await msg.answer(f'Ты выбрала {msg.text.lower()} {user_data["love_choise"]}',reply_markup=types.ReplyKeyboardRemove())
    await msg.answer('Я тебя сильнее \U0001F48B	')
    await state.finish()

async def cancel_cmd(msg:types.Message,state:FSMContext):
    await state.finish()
    await msg.answer('Отменено',reply_markup=types.ReplyKeyboardRemove())


dp.register_message_handler(cancel_cmd,commands='cancel',state='*')
dp.register_message_handler(lovestart,commands='love',state="*")
dp.register_message_handler(lovechoise,state=Orderlove.waiting_for_messange)
dp.register_message_handler(love_size_choise,state=Orderlove.waiting_for_size)



if __name__ == '__main__':
   executor.start_polling(dp)