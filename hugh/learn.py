from .cobe.brain import Brain

BOT_BRAIN_ID = 'test'
brain_path = f'data/brain/{BOT_BRAIN_ID}'
brain = Brain(brain_path)

files = [f for f in os.listdir('to_import')]
for i in files:
    with open(f'to_import/{i}', 'r') as f:
        for line in f:
            brain.learn(line)
