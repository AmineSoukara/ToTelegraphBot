# (c) 

import os
import uuid
import shutil
import logging
import traceback
from pyrogram import Client, filters
from creds import Credentials
from telegraph import upload_file
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)


TGraph = Client(
    "Image upload bot",
    bot_token=Credentials.BOT_TOKEN,
    api_id=Credentials.API_ID,
    api_hash=Credentials.API_HASH,
)

UPDATES_CHANNEL = os.environ.get('UPDATES_CHANNEL', 'DamienSoukara')
home_text = """
Hi, [{}](tg://user?id={})

I Am Telegra.ph Image Uploader Bot.

Send Me Any Image I Will Upload It To Telegra.ph.
"""
about_text = """
🤖 **My Name:** [Telegraph Image Bot](https://t.me/ToTelegraphBot)

📝 **Language:** [Python 3](https://www.python.org)

📚 **Framework:** [Pyrogram](https://github.com/pyrogram/pyrogram)

📡 **Hosted on:** [Heroku](https://www.heroku.com)

👨‍💻 **Developer:** @AmineSoukara

👥 **Support Group:** [Damien Help](https://t.me/DamienHelp)

📢 **Updates Channel:** [Damien Soukara](https://t.me/DamienSoukara)
"""

@TGraph.on_message(filters.command("start"))
async def start(client, message):
    ## Doing Force Sub 🤣
    update_channel = UPDATES_CHANNEL
    if update_channel:
        try:
            user = await client.get_chat_member(update_channel, message.chat.id)
            if user.status == "kicked":
               await client.send_message(
                   chat_id=message.chat.id,
                   text="Sorry, You Are Banned!\nYou Can't Use Me. Contact My [Owner](https://t.me/DamienRobot).",
                   parse_mode="markdown",
                   disable_web_page_preview=True
               )
               return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.chat.id,
                text="**Please Join My Updates Channel To Use This Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("💬 Join Updates Channel", url=f"https://t.me/{update_channel}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.chat.id,
                text="Something Went Wrong. Contact My [Owner](https://t.me/DamienRobot).",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    ##
    await message.reply_text(
        f"Hi, {message.from_user.mention}.\n\nI Am Telegra.ph Image Uploader Bot.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="💬 Updates Channel", url="https://t.me/DamienSoukara"),
                    InlineKeyboardButton(text="🗣 Support Group", url="https://t.me/DamienHelp")
                ],
                [
                    InlineKeyboardButton("©️ About", callback_data="about")
                ]
            ]
        ),
        parse_mode="html",
        disable_web_page_preview=True
    )


@TGraph.on_message(filters.private & (filters.photo | filters.document))
async def getimage(client, message):
    ## Doing Force Sub 🤣
    update_channel = UPDATES_CHANNEL
    if update_channel:
        try:
            user = await client.get_chat_member(update_channel, message.chat.id)
            if user.status == "kicked":
               await client.send_message(
                   chat_id=message.chat.id,
                   text="Sorry, You are Banned!\nYou Can't Use Me. Contact My [Owner](https://t.me/DamienRobot).",
                   parse_mode="markdown",
                   disable_web_page_preview=True
               )
               return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.chat.id,
                text="**Please Join My Updates Channel To Use This Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("💬 Join Updates Channel", url=f"https://t.me/{update_channel}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.chat.id,
                text="Something Went Wrong. Contact My [Owner](https://t.me/Damienrobot).",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    ##
    if message.document:
        if not message.document.file_name.endswith(".jpg"):
            return
    tmp = os.path.join("downloads", str(message.chat.id))
    if not os.path.isdir(tmp):
        os.makedirs(tmp)
    img_path = os.path.join(tmp, str(uuid.uuid4()) + ".jpg")
    dwn = await message.reply_text("⏳ Downloading ...", True)
    img_path = await client.download_media(message=message, file_name=img_path)
    await dwn.edit_text("✅ Uploading ...")
    try:
        response = upload_file(img_path)
    except Exception as error:
        await dwn.edit_text(f"Oops, Something Went Wrong!\n\n{error}")
        return
    await dwn.edit_text(f"https://telegra.ph{response[0]}")
    shutil.rmtree(tmp, ignore_errors=True)

## The Callback Thing
#############################################
def dynamic_data_filter(data):
    async def func(flt, _, query):
        return flt.data == query.data

    return filters.create(func, data=data)
#############################################

@TGraph.on_callback_query(dynamic_data_filter("about"))
async def about_meh(_, query):
    buttons = [
        [
            InlineKeyboardButton("🏠 Home", callback_data="home"),
            InlineKeyboardButton("⛔ Close", callback_data="closeit")
        ]
    ]
    await query.message.edit(
        about_text,
        parse_mode="markdown",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    await query.answer()

@TGraph.on_callback_query(dynamic_data_filter("home"))
async def go_to_home(_, query):
    buttons = [
        [
            InlineKeyboardButton("🗣 Support Group", url="http://t.me/damienhelp"),
            InlineKeyboardButton("💬 Updates Channel", url="http://t.me/Damiensoukara")
        ],
        [
            InlineKeyboardButton("©️ About", callback_data="about")
        ]
    ]
    await query.message.edit(
        home_text.format(query.message.chat.first_name, query.message.chat.id),
        parse_mode="markdown",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await query.answer()

@TGraph.on_callback_query(dynamic_data_filter("closeit"))
async def closeme(_, query):
    await query.message.delete()
    await query.answer()
##

TGraph.run()
