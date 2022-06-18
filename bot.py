import os
import logging

from aiogram import Bot, Dispatcher, executor, types

from trans import transliteration_dict


HELLO = """Если вы покупаете авиабилет на внутренний паспорт или свидетельство \
о рождении, вы можете внести данные латинскими буквами, используя правила \
транслитерации, установленные Приказом МИД России от 12.02.2020 № 2113. \

Отправь мне полное ФИО и я транслитерирую их в соответствии с правилами."""
        
TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    text = f'Привет, {user_name}!'
    logging.info(f'Start message from {user_name=}, {user_id=}')
    await message.reply(text)
    await bot.send_message(user_id, HELLO)
    
@dp.message_handler()
async def make_echo(message):
    chat_id = message.from_user.id
    fio = message.text
    logging.info(f'{fio=} from {chat_id=}')
    translit = ''
    try:
        for i in fio.split():
            translit += ' '+''.join([transliteration_dict[j.upper()] for j in i])
            translit = translit.strip()
    except:
        translit = 'Не удалось транслитерировать. Попробуйте еще раз написать ФИО только на кириллице'  
    
    logging.info(f'{translit=}')
    await bot.send_message(chat_id, translit)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)