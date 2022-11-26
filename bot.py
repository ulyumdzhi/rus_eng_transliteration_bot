import os
import logging
import asyncio
from string import punctuation

from aiogram import Bot, Dispatcher, executor, types

from trans import FAIL
from utils import trans_checker


HELLO = """Если вы покупаете авиабилет на внутренний паспорт или свидетельство \
о рождении, вы можете внести данные латинскими буквами, используя правила \
транслитерации, установленные Приказом МИД России от 12.02.2020 № 2113. \
\n
*Отправь мне ФИО на русском (кириллицей)*
A я транслитерирую их в соответствии с [правилами](https://www.consultant.ru/document/cons_doc_LAW_360580/9eb761ae644ec1e283b3a50ef232330b924577cb/)."""


logging.basicConfig(level=logging.INFO, 
                    filename='translit.log')

TOKEN = os.environ['TOKEN']

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    text = f'Привет, {user_name}!'
    logging.info(f'Start message from {user_name=}, {user_id=}')
    
    await message.reply(text)
    await asyncio.sleep(2)
    await bot.send_message(user_id, HELLO, 
                           parse_mode='Markdown',
                           disable_web_page_preview=True)
    
    
@dp.message_handler()
async def translit_this(message):
    chat_id = message.from_user.id
    fio = message.text
    fio = [word.upper() for word in fio.split()]
       
    logging.info(f'{fio=} from {chat_id=}')
    translit = ' '
    _translit = []
    try:
        for word in fio:
            code, result = trans_checker(word)
            
            if code:
                _translit.append(result)
            else:
                raise ValueError(f'{word}: символ "{word[result]}"')
        
        translit = translit.join(_translit)
        
    except Exception as e:
        translit = FAIL.format(e)
    
    logging.info(f'{translit=}')
    await bot.send_message(chat_id, translit)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
