import json
from pprint import pprint
from app import config
from app import unimatrix as u


drone = u.Markov(BOT_BRAIN_ID)

files = [f for f in os.listdir('to_import')]
for i in files:
    with open(f'to_import/{i}', 'r') as f:
        content = json.loads(f.read())
    for message in messages:
        print('learning...')
        markov.learn(message)
