from discord import Message
from discord.ext import commands
#from command_list import get_command
from responses import get_response
from dotenv import load_dotenv
import os
from typing import Final
import logging

load_dotenv()

CREATOR_ID: Final[int] = int(os.getenv("CREATOR_ID"))


async def send_message(message: Message, user_message: str, bot: commands.Bot) -> None:
    if not user_message:
        logging.warning("Message is empty... check intents and debug")

    if user_message[0] == '!':
        await message.channel.send("'!' commands have been depriciated and are no longer functional. Please use '/' commands instead.")

    try:
        response = get_response(user_message)
        if not response:
            return
        await message.channel.send(response)
    except Exception as e:
        logging.error(e)


async def send_feedback(feedback: str, bot: commands.Bot) -> None:
    creator_id = CREATOR_ID
    user = await bot.fetch_user(creator_id)
    if user:
        await user.send(feedback)
