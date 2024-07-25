import asyncio
import os
from typing import Final
from datetime import datetime, time, timedelta
from discord.ext import commands
import random
from dotenv import load_dotenv
import logging

load_dotenv()

'''This should only be used for testing purposes.'''
GENERAL_ID: Final[int] = int(os.getenv("DISCORD_TEST_CHANNEL_ID"))
#GENERAL_ID: Final[int] = int(os.getenv("WESLEY_GENERAL"))


async def schedule_daily_message(bot: commands.Bot):
    now = datetime.now()
    target_time = time(12, 0)
    today_target = datetime.combine(now.date(), target_time)

    if now > today_target:
        today_target += timedelta(days=1)

    wait_time = (today_target - now).total_seconds()
    await asyncio.sleep(wait_time)

    while True:
        await send_daily_message(bot)
        await asyncio.sleep(24 * 3600)


async def schedule_customs_message(bot: commands.Bot):
    now = datetime.now()
    target_time = time(13, 30)
    today_target = datetime.combine(now.date(), target_time)

    if now > today_target:
        today_target += timedelta(days=1)

    wait_time = (today_target - now).total_seconds()
    await asyncio.sleep(wait_time)

    while True:
        await send_customs_message(bot)
        await asyncio.sleep(3 * 24 * 3600)


async def schedule_weekly_message(day_of_week, target_time, message, bot: commands.Bot):
    now = datetime.now()
    today_target = datetime.combine(now.date(), target_time)
    days_until_target = (day_of_week - today_target.weekday() + 7) % 7

    # If today is the target day and the target time has already passed, schedule for the next week
    if days_until_target == 0 and now > today_target:
        days_until_target = 7

    # Schedule for the upcoming target day
    next_target = today_target + timedelta(days=days_until_target)
    wait_time = (next_target - now).total_seconds()
    await asyncio.sleep(wait_time)

    while True:
        await send_weekly_message(message, bot)
        await asyncio.sleep(7 * 24 * 3600)  # Sleep for 7 days


async def send_weekly_message(message: str, bot: commands.Bot):
    channel = bot.get_channel(GENERAL_ID)
    if channel:
        await channel.send(message)
        logging.info(f"Sent weekly message '{message}' to {channel.name}.")
    else:
        logging.warning("General Channel not found in Wesley server.")


async def send_daily_message(bot: commands.Bot):
    channel = bot.get_channel(GENERAL_ID)
    if channel:
        responses = [
            "I'm going to your funeral whether you like it or not.",
            "That'll put a little clap in your trap.",
            "Stoning and getting stoned are two very different things",
            "Lesson of the day: I'm not your peer and I will ruin you.",
            "Chicken and waffles make me snarky. Just naming it",
            "We go. No come.",
            "I let my freak flag fly."
        ]
        response = random.choice(responses)
        await channel.send(response)
        logging.info(f"Sent weekly message '{response}' to {channel.name}.")
    else:
        logging.warning("General Channel not found in Wesley server.")


async def send_customs_message(bot: commands.Bot):
    channel = bot.get_channel(GENERAL_ID)
    if channel:
        responses = [
        "Hey pookies! Could use some help with Customs today if anyone is available!",
        "Hi friends! Could anyone possibly help us table at Customs today?",
        "Hey everyone! Could one of you possibly help us with Customs at the STU today?"
    ]
        response = random.choice(responses)
        await channel.send(response)
        logging.info(f"Sent CUSTOMS message '{response}' to {channel.name}.")
    else:
        logging.warning("General Channel not found in Wesley server.")
