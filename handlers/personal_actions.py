from aiogram import types
from dispatcher import dp

import config
import re
from bot import BotDB

@dp.message_handler(commands = "start")
async def start(message: types.Message):
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)

    await message.bot.send_message(message.from_user.id, "Добро пожаловать!")

@dp.message_handler(commands = ("spend", "earn", "s", "e"), commands_prefix = "/!")
async def start(message: types.Message):
    cmd_variants = (('/spend', '/s', '!spend', '!s'), ('/earn', '/e', '!earn', '!e'))
    operation = '-' if message.text.startswith(cmd_variants[0]) else '+'
    source = message.text.split( )
    source = source[2]

    value = message.text
    for i in cmd_variants:
        for j in i:
            value = value.replace(j, '').strip()

    if(len(value)):
        x = re.findall(r"\d+(?:.\d+)?", value)
        if(len(x)):
            value = float(x[0].replace(',', '.'))

            BotDB.add_record(message.from_user.id, operation, value, source)

            if(operation == '-'):
                await message.reply("✅ Запись о <u><b>расходе</b></u> успешно внесена!")
            else:
                await message.reply("✅ Запись о <u><b>доходе</b></u> успешно внесена!")
        else:
            await message.reply("Не удалось определить сумму!")
    else:
        await message.reply("Не введена сумма!")

@dp.message_handler(commands = ("history", "h"), commands_prefix = "/!")
async def start(message: types.Message):
    cmd_variants = ('/history', '/h', '!history', '!h')
    within_als = {
        "day": ('today', 'day', 'сегодня', 'день'),
        "month": ('month', 'месяц'),
        "year": ('year', 'год'),
    }

    cmd = message.text
    for r in cmd_variants:
        cmd = cmd.replace(r, '').strip()

    within = 'day'
    if(len(cmd)):
        for k in within_als:
            for als in within_als[k]:
                if(als == cmd):
                    within = k

    records = BotDB.get_records(message.from_user.id, within)
    balance = 0
    if(len(records)):
        answer = f"🕘 История операций за {within_als[within][-1]}\n\n"

        for r in records:
            answer += "<b>" + ("➖ Расход" if not r[2] else "➕ Доход") + "</b>"
            answer += f" - {r[3]}"
            answer += f" <i>({r[4]})</i>"
            answer += f"{r[5]}\n"
            if not r[2]:
                balance = balance - r[3]
            else:
                balance = balance + r[3]
        answer += f"\nБаланс: {balance}\n"
        await message.reply(answer)
    else:
        await message.reply("Записей не обнаружено!")

@dp.message_handler(commands=("balance", "b"), commands_prefix="/!")
async def start(message: types.Message):
    cmd_variants = ('/balance', '/b', '!balance', '!b')
    balance = 0
    records = BotDB.get_records(message.from_user.id)
    if (len(records)):
        for r in records:
            if not r[2]:
                balance = balance - r[3]
            else:
                balance = balance + r[3]
        await message.reply(balance)

@dp.message_handler(commands=("help"), commands_prefix="/!")
async def start(message: types.Message):
    cmd_variants = ('/help', '!help')