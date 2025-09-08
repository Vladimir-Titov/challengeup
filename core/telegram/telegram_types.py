from typing import TypedDict


class User(TypedDict, total=False):
    id: int
    is_bot: bool
    first_name: str
    last_name: str
    username: str
    language_code: str
    is_premium: bool


class Chat(TypedDict, total=False):
    id: int
    last_name: str
    first_name: str
    username: str
    type: str


class MessageEntity(TypedDict, total=False):
    type: str
    offset: int
    length: int


class Message(TypedDict, total=False):
    message_id: int
    from_: User
    date: int
    chat: Chat
    text: str
    entities: list[MessageEntity]


class CallbackQuery(TypedDict, total=False):
    id: str
    from_: User
    message: Message
    chat_instance: str
    data: str


class Update(TypedDict, total=False):
    update_id: int
    message: Message
    callback_query: CallbackQuery


class InlineKeyboardButton(TypedDict, total=False):
    text: str
    url: str
    callback_data: str


class InlineKeyboardMarkup(TypedDict, total=False):
    inline_keyboard: list[list[InlineKeyboardButton]]
