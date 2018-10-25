import os

SLACK_API_TOKEN = os.environ['SLACK_BOT_TOKEN']
BOT_USER_NAME = os.getenv('SLACK_BOT_NAME', 'hugh')
BOT_BRAIN_ID = os.getenv('SLACK_BOT_BRAIN_ID', 'hugh')
SLEEP_TIME = float(os.getenv('SLACK_BOT_SLEEP', '0.1'))

