from robocorp.actions import action
from RPA.Notifier import Notifier
import os
from dotenv import load_dotenv


@action
def slack_message(message: str, channel: str = "mika-dev") -> str:
    """
    Send a message to a Slack channel.

    :param message: message to send
    :param channel: channel to send message to
    :return: empty string on success, error message on failure

    """
    load_dotenv()
    slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    try:
        Notifier().notify_slack(
            message=message, channel=channel, webhook_url=slack_webhook_url
        )
    except Exception as exc:
        return str(exc)
    return ""
