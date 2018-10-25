import re
import logging
import time

from . import config, slack

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
alerts = []


def get_username_by_id(userid):
    userinfo = slack.client.api_call('users.info', user=userid)
    username = userinfo['user']['name']
    return username

def record_alert(event):
    global alerts

    logger.debug(event)

    for attachment in event['attachments']:
        alert_name = re.search('((?:[\w\-.0-9_]+)\/(?:[a-z\-.0-9_]+))', attachment['title']).group()
        alert_status = re.search('(OK|CRITICAL)', attachment['title']).group()
        if alert_status == "CRITICAL":
            existing_alert = list(filter(lambda alert: alert['name'] == alert_name, alerts))
            if existing_alert:
                existing_alert[0]['occurrences'] += 1
            else:
                alerts += [{'name': alert_name, 'occurrences': 1}]
    print('Current alerts record %s', alerts)
    return

def reply(event):
    global alerts
    user_id = event['user']
    text = event['text'].strip(config.BOT_USER_NAME+' ')
    channel_id = event['channel']   

    if re.search('(alert report)',text):
        if alerts:
            alerts_sorted = sorted(alerts, key=lambda k: k['occurrences']) 
            report = ''
            for alert in alerts_sorted:
                report = report+'Alert: '+alert['name']+' - Occurrences:'+str(alert['occurrences'])+'\n'
            slack.client.api_call(
                'chat.postMessage',
                channel=channel_id,
                text='Here are all the alerts I\'ve recorded so far: ```'+report+'```',
                as_user=True,
                mrkdwn=True
            )
        else:
            slack.client.api_call(
                'chat.postMessage',
                channel=channel_id,
                text='No alerts recorded so far',
                as_user=True,
                mrkdwn=True
            )
        return

    slack.client.api_call(
        'chat.postMessage',
        channel=channel_id,
        text='Not entirely sure what you mean '+get_username_by_id(user_id),
        as_user=True,
        mrkdown=True
    )
    return

def understand(event):
    if not 'type' in event:
        return

    logger.debug('Processing new %s event', event['type'])

    if event['type'] == 'message':
        if 'subtype' in event and event['subtype'] == 'bot_message':
            bot_id = event['username']
        else:
            user_id = event['user']
        text = event['text']
        channel_id = event['channel']   
    
        if 'subtype' in event and event['subtype'] == 'bot_message':
            if bot_id == 'sensu-alerts':
                record_alert(event)
        
        if re.match(config.BOT_USER_NAME,text):
            logger.info('Someone is talking to me')
            reply(event)

    return

def run():
    slack.init()

    try:
        slack.client.rtm_connect()
    except:
        logger.exception('Failed to connect to Slack!')

    logger.info('Connected to Slack, ready to roll!')

    while True:
        stream = slack.client.rtm_read()
        for event in stream:
            try:
                understand(event)
            except KeyboardInterrupt:
                logger.info('Exiting gracefully')
                return
            except:
                logger.exception('Failed to process this event')

        try:
            time.sleep(config.SLEEP_TIME)
        except KeyboardInterrupt:
            logger.info('Exiting gracefully')
            return




