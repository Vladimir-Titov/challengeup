import re

from core.telegram.telegram_types import Message


def regex_match(regex: str, message: Message) -> bool:
    if re.match(regex, message['text']) is not None:
        return True
    return False


def command_match(commands: list[str], message: Message) -> bool:
    if message['text'] in commands:
        return True
    return False
