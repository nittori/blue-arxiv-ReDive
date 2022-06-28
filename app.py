import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import time
import datetime
import get_paper

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)
# ID of the channel you want to send the message to
channel_id = os.environ.get("channel_id")#slackのチャンネルID

def post_message(message):
    try:
        # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel=channel_id, 
            text=message
        )
        logger.info(result)
    
    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")

def main():
    papers = get_paper.get_paper()
    
    if len(papers) == 0:
        return 0
    else:
        for paper in papers:
            message = f"author : {paper['author']}\n"+\
                      f"publish_date : {paper['published']}\n"+\
                      f"title : {paper['title']}\n"+\
                      f"url : {paper['url']}\n"
            print(message)
            #post_message(message)
        return 1
    
if __name__ == "__main__":
    main()
        