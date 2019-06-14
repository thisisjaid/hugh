import re
import logging
from .cobe.brain import Brain
from .config import *

brain_path = f'data/brain/{BOT_BRAIN_ID}'
os.makedirs('data/brain/', exist_ok=True)

hugh = Brain(brain_path)

def filter(message):
    message = re.sub('\<@[A-Z0-9a-z]{9}\>', '', message) # remove mentions
    message = re.sub('\s{2,}', ' ', message) #remove double spaces
    message = re.sub('\<[^\<]+\>', '', message) #remove links
    message = message.strip() # remove unneeded spaces
    valid = False
    if len(message) > 5:
        valid = True
    if re.search('(hubot)',message):
        valid = False
    return valid,message

def learn(message):
    global hugh
    valid, message = filter(message)
    if not valid:
        return
    logger.info('Learning message - '+text)
    hugh.learn(message)

def backtalk(message):
    global hugh
    response = hugh.reply(message, loop_ms=1000, max_len=100)
    valid, response = filter(response)
    if not valid:
        return None
    return response
