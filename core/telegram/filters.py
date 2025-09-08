import re

from core.telegram.telegram_types import Update


def regex_match(regex: str, message: Update) -> bool:
    if re.match(regex, message.get('message', {}).get('text')) is not None:
        return True
    return False


def command_match(commands: list[str], message: Update) -> bool:
    if message.get('message', {}).get('text') in commands:
        return True
    return False


def callback_match(callback_data: str, message: Update) -> bool:
    callback = message.get('callback_query')
    if callback is not None and callback['data'] == callback_data:
        return True
    return False
