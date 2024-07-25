import random
import logging

def get_response(user_input: str) -> str:
    lowered = user_input.lower()

    if lowered == "hello world":
        return "Hello, I heard you!"
    elif lowered == "hi john!":
        responses = [
            "Hey friends!",
            "Hey guys!",
            "Hey pookie!",
            "Whats up guys?!"
        ]
        return random.choice(responses)
    else:
        if random_num := random.randint(1, 100) <= 5:
            logging.info("CASE PASSED: Sending Awesome message!")
            return "That's awesome!"
        else:
            return
