import logging
from slackclient import SlackClient

from . import config

logger = logging.getLogger(__name__)

def init():
    global client
    client = SlackClient(config.SLACK_API_TOKEN)

def make_api_call(*args, **kwargs):
    res = client.api_call(*args, **kwargs)
    assert res['ok'] == True, res
    return res


