import certifi  #To get SSL certificate
from dotenv import load_dotenv  #To load our environment variables
from typing import Final  #Typing to create a Final (const) type
import os  #OS is used to get environment variables
from discord import Intents, Message, Member, utils, Game, app_commands  #Discord Package
from discord.ext import commands  #Framework for command handling
import aiojobs  #Create schedules for big-3 events
from datetime import time, datetime
import asyncio  #Used for sleep function
import random
import console
import scheduled_announcements
import helper_funcs
import logging

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_filename = os.path.join(log_dir, f"LOG_{datetime.now():%Y-%m-%d_%H-%M-%S}.txt")
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

load_dotenv()
os.environ['SSL_CERT_FILE'] = certifi.where()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
CREATOR_ID: Final[int] = int(os.getenv("CREATOR_ID"))

intents = Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_member_join(member: Member) -> None:
    welcome_channel = utils.get(member.guild.channels, name="welcome")
    if welcome_channel:
        await welcome_channel.send(f"Hey, I'm John! We're so glad you're here {member.mention}!")


@bot.event
async def on_ready() -> None:
    print(f"Bot successfully logged in as {bot.user}")
    creator_id = CREATOR_ID
    '''These should only be used on the test bot'''
    #user = await client.fetch_user(creator_id)
    #if user:
    #await user.send("John is online.")

    print("Syncing Commands...", end='', flush=True)
    await bot.tree.sync()  # Sync the slash commands
    print("\rSyncing Commands...DONE!")

    activity = Game("/help")
    await bot.change_presence(activity=activity)

    scheduler = await aiojobs.create_scheduler()
    await scheduler.spawn(scheduled_announcements.schedule_weekly_message(day_of_week=1,
                                                                          target_time=time(18, 30),
                                                                          message="Worship in 30 minutes! Hope to see y'all there!!",
                                                                          bot=bot))
    await scheduler.spawn(scheduled_announcements.schedule_weekly_message(day_of_week=2,
                                                                          target_time=time(10, 30),
                                                                          message="FREE Lunch in 30 minutes! Hope to see y'all there!!",
                                                                          bot=bot))
    await scheduler.spawn(scheduled_announcements.schedule_weekly_message(day_of_week=3,
                                                                          target_time=time(17, 30),
                                                                          message="Dinner & Bible Study in 30 minutes! Hope to see y'all "
                                                                                  "there!!", bot=bot))
    await scheduler.spawn(scheduled_announcements.schedule_daily_message(bot))
    await scheduler.spawn(scheduled_announcements.schedule_customs_message(bot))

    await asyncio.create_task(console.console_listener(bot))


@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return

    username: str = str(message.author)
    user_message: str = str(message.content)
    channel: str = str(message.channel)

    await helper_funcs.send_message(message, user_message, bot)


# Slash command to ping
@bot.tree.command(name="ping", description="Replies with pong and latency to server!")
async def ping(interaction):
    await interaction.response.send_message(f"pong! Latency is {(bot.latency * 1000):.2f}ms", ephemeral=True)
    logging.info(f"{interaction.user} used command /ping.")


@bot.tree.command(name="help", description="Displays the list of commands")
async def help(interaction):
    await interaction.response.send_message(
        "Commands:\n\n/help: Displays a list of commands\n/welcome: Sends a welcome message\n/communion: Sends "
        "a quote from Communion nights\n/ping: Replies 'pong' with the latency in milliseconds\n/quote: Sends "
        "a random John quote\n/feedback"
        "<feedback_here>: Sends feedback to Alec. These can be suggestions, bugs, or whatever really!\n/version: "
        "Sends the current version of John Bot.\n/new: Displays what is new with John Bot.\n"
        "/customs: Sends a quote from CUSTOMS.", ephemeral=True)
    logging.info(f"{interaction.user} used command '/help'.")


@bot.tree.command(name="welcome", description="Sends a welcome message!")
async def welcome(interaction):
    await interaction.response.send_message("Hey, I'm John. We're so glad that you're here!")
    logging.info(f"{interaction.user} used command '/welcome'.")


@bot.tree.command(name="communion", description="Sends a quote from communion nights")
async def communion(interaction):
    await interaction.response.send_message("Come like its your first time, come like its your last.")
    logging.info(f"{interaction.user} used command '/communion'.")


@bot.tree.command(name="quote", description="Sends a random John quote!")
async def quote(interaction):
    responses = [
        "I'm going to your funeral whether you like it or not.",
        "That'll put a little clap in your trap.",
        "Stoning and getting stoned are two very different things.",
        "Lesson of the day: I'm not your peer and I will ruin you.",
        "Chicken and waffles make me snarky. Just naming it.",
        "We go. No come.",
        "I let my freak flag fly."
    ]

    await interaction.response.send_message(random.choice(responses))
    logging.info(f"{interaction.user} used command '/quote'.")


@bot.tree.command(name="version", description="Sends the current version of John Bot")
async def version(interaction):
    await interaction.response.send_message("Currently Running Version 0.3 of John Bot.",
                                            ephemeral=True)
    logging.info(f"{interaction.user} used command '/version'.")


@bot.tree.command(name="new", description="Displays what is new with John Bot")
async def new(interaction):
    await interaction.response.send_message("What's new in 0.3:\n\n-CUSTOMS quotes are here! They will appear every 3 days at 1:30PM or can be triggered with /customs!\n"
                                            "-Project moved to a new software for development.\n-'!' commands are no longer supported.", ephemeral=True)
    logging.info(f"{interaction.user} used command '/new'.")


@bot.tree.command(name="feedback", description="Sends feedback to the developer of John Bot (Alec).")
@app_commands.describe(feedback="Your feedback to be sent")
async def feedback(interaction, feedback: str):
    creator_id = CREATOR_ID
    creator = await bot.fetch_user(creator_id)

    if creator:
        await creator.send(f"Feedback from {interaction.user}: {feedback}")
        await interaction.response.send_message("Thank you for your feedback!", ephemeral=True)
        logging.info(f"{interaction.user} used command '/feedback' with message {feedback}.")
    else:
        await interaction.response.send_message("Error sending feedback, please try again later", ephemeral=True)
        logging.error(f"{interaction.user} used command '/feedback'. Feedback was unable to be sent.")


@bot.tree.command(name="customs", description="Sends a quote from CUSTOMS.")
async def customs(interaction):
    responses = [
        "Hey pookies! Could use some help with Customs today if anyone is available!",
        "Hi friends! Could anyone possibly help us table at Customs today?",
        "Hey everyone! Could one of you possibly help us with Customs at the STU today?"
    ]
    await interaction.response.send_message(random.choice(responses))
    logging.info(f"{interaction.user} used command '/customs'.")


def main():
    print("Welcome to John Bot v0.3")
    print("NOTE: Bot is still EARLY in development. Use /feedback to report issues or request features.")
    bot.run(token=TOKEN)


if __name__ == '__main__':
    main()
