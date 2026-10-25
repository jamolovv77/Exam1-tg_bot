from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
from service import *
from connection import create_table
import asyncio
import os


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()



main_menu = ReplyKeyboardMarkup(
    keyboard=[


        [KeyboardButton(text="🎟️ chorabini")],
        [KeyboardButton(text="📋 naviwtahoi man")]
    ]


)



@dp.message(CommandStart())
async def cmd_start(message: Message):
    await create_table()



    await message.answer(
        "SALOM 👋 man boti wumo baroi dobavit kardani chorabiniho hastam 🎟️\n"
        reply_markup=main_menu



    )


@dp.message(Command("add_event"))
async def cmd_add_event(message: Message, comand: CommandObject):
    parts = comand.args.split("|")

    if len(parts) != 3:
        await message.answer(
            "❌ malumotatonro bo alomati  | judo kuned."
        )
        return
    try:
        title = parts[0].strip()
        capacity = int(parts[1].strip())
        event_date = parts[2].strip()

        if capacity <= 0:
            await message.answer(
                "Wumorai joyho boyad ay 0 biso bowad ⚠️!"

            )

        await add_envent_db(title, capacity, event_date)

        await message.answer(
            f"Chorabini {title} ilova karda wud ✅"

        )

    except Exception as Eror:
        await message.answer(f"Xato: {Eror}")





@dp.message(Command("events"))
@dp.message(F. text == "🎟️ chorabini")
async def cmd_events(message:Message):
    events = await get_all_events_db()


    if len (events) ==0:
        await message.answer(
            "Holo yagon chorabini nest !"
        )

        for event in events:
            text+=(
            f"-----------------\n"
            f"🆔 ID: {event['id']}\n"
            f"📌 NOM: {event['title']}\n"
            f"👥 JOYHO: {event['capacity']}\n"
            f"📅 SANA: {event['event_date']}\n"
            "------------------\n"

            )
     


    text +="\nbaroi dobavit kardani xud xudatonro nomnavis kund:\n/register ID"



    await message.answer(text)


@dp.message(Command("register"))
async def cmd_register(message: Message, command: CommandObject):





    event_id = int(command.args)
    user_id = str(message.from_user.id)




    status = await register_user_db(user_id,event_id)

    if status =="not_found":
        await message.answer(
            " yagon Chorabiniho yoft nawudand ❌"
        )


    elif status == "already_registered":
        await message.answer(
            "Wumo uzhe dobaivt wudagiyed"
        )

    elif status == "waitlist":
            await message.answer(
                "joyho zanit wudan wmo metoned da ruyxati zaprosho dobavit waved"

        )





@dp.message(Command("cancel"))
async def cmd_cancel (message: Message,command: CommandObject):
    event_id = int(command.args)
    user_id = str(message.from_user.id)

    
    old_status, promoted_user_id = await cancel_registration_db(
        user_id, event_id)


    if old_status is None:
        await message.answer(
            "wumo xudatonro dar in chorabini dobavit nakadagiend"
        )


    if promoted_user_id is not None:
        try:
            await bot.send_message(
                int(promoted_user_id),
                "joy xoli wud zaprosi wumo baroi dobavit wudan kabul wud ✅"


            )
        except Exception:
            pass


@dp.message(Command("my_events"))
@dp.message(F.text == "📋 naviwtahoi man")

async def cmd_my_events(message:Message):
    user_id = str(message.from_user.id)



    events = await get_user_events_db(user_id)



    if len(events) == 0:
        await message.answer(
            "wmo oli dobavit nakardaen xudatonro"
        )

        








    








