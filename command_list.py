'''
!!!>>> '!' COMMANDS ARE NO LONGER SUPPORTED. THIS FILE IS FOR DOCUMENTATION PURPOSES ONLY <<<!!!

import random
from discord import Client


def get_command(user_input: str, client: Client) -> str:
    lowered = user_input.lower()

    if lowered == "!help" or lowered == "!h":
        return ("Commands:\n\n/help: Displays a list of commands\n/welcome: Sends a welcome message\n/communion: Sends "
                "a quote from Communion nights\n/ping: Replies 'pong' with the latency in milliseconds\n/quote: Sends "
                "a random John quote\n/feedback"
                "<feedback_here>: Sends feedback to Alec. These can be suggestions, bugs, or whatever "
                "really!\n/version: Sends the current version of John Bot.\n/new: Displays what is new with John Bot.")
    elif lowered.startswith("!feedback"):
        feedback = user_input[len("!feedback "):].strip()
        if feedback:
            return "FEEDBACK: " + feedback
        else:
            return ("Incorrect usage of the !feedback command. Please use !feedback <feedback_here> or !f "
                    "<feedback_here>")
    elif lowered.startswith("!f"):
        feedback = user_input[len("!f "):].strip()
        if feedback:
            return "FEEDBACK: " + feedback
        else:
            return ("Incorrect usage of the !feedback command. Please use !feedback <feedback_here> or !f "
                    "<feedback_here>")
    elif lowered == "!welcome" or lowered == "!w":
        return "Hey, I'm John. We're so glad that you're here!"
    elif lowered == "!communion" or lowered == "!c":
        return "Come like its your first time, come like its your last."
    elif lowered == "!ping" or lowered == "!p":
        return f"pong! (Latency is {(client.latency * 1000):.2f}ms)"
    elif lowered == "!quote" or lowered == "!q":
        responses = [
            "I'm going to your funeral whether you like it or not.",
            "That'll put a little clap in your trap.",
            "Stoning and getting stoned are two very different things.",
            "Lesson of the day: I'm not your peer and I will ruin you.",
            "Chicken and waffles make me snarky. Just naming it.",
            "We go. No come.",
            "I let my freak flag fly."
        ]
        return random.choice(responses)
    elif lowered == "!version" or lowered == "!v":
        return "Currently Running Version 0.1.5 of John Bot."
    elif lowered == "!new" or lowered == "!n":
        return ("What's new in 0.1.5:\n\n-Fixed a bug where the /feedback command did not exist.")
    else:
        return "I'm sorry, I do not know that command!"
'''