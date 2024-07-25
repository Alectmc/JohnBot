from discord.ext import commands
import asyncio
import logging

#This is the test send_global_message function
'''async def send_global_message(message: str, bot: commands.Bot):
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.name == "test_john":
                try:
                    await channel.send(message)
                    print(f"Sent message '{message}' to {channel.name} in {guild.name}")
                except Exception as e:
                    print(f"ERROR: Failed to send message '{message}' to {channel.name} in {guild.name}")
                break'''


#This is the official send_global_message function
async def send_global_message(message: str, bot: commands.Bot):
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.name == "general":
                try:
                    await channel.send(message)
                    print(f"Sent message '{message}' to {channel.name} in {guild.name}")
                    logging.info(f"Sent message '{message}' to {channel.name} in {guild.name}")
                except Exception as e:
                    print(f"ERROR: Failed to send message '{message}' to {channel.name} in {guild.name}: {e}")
                    logging.error(f"ERROR: Failed to send message '{message}' to {channel.name} in {guild.name}: {e}")
                break


async def console_listener(bot: commands.Bot):
    print("WARNING: Console is in EARLY stages. Please use caution!")

    while True:
        command = await asyncio.to_thread(input, "> ")
        command = command.strip()
        if command == "help":
            print("COMMANDS:\n\nmsg <message>: Sends a global message to all server John Bot is in with a general "
                  "chat.\nshutdown: Shuts down John Bot safely.\nversion: Prints the current version of John Bot.")
        elif command == "shutdown":
            print("Shutting Down...")
            await bot.close()
            break
        elif command.startswith("msg"):
            message = command[len("msg "):]
            if message:
                await send_global_message(message, bot)
            else:
                print("No message provided for msg command.")
        elif command == "version":
            print("Currently running John Bot 0.1.5")
        else:
            print(f"Unknown command: {command}")
