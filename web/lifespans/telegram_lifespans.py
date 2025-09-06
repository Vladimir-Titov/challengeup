from settings.db import db_config
from settings.telegram import telegram_config
from web.lifespans.db import db_init
from web.lifespans.dispatcher import dispatcher_init


class TelegramLifespans:
    @property
    def db(self):
        return db_init('db_pool', db_config.model_dump())

    @property
    def dispatcher(self):
        return dispatcher_init('dispatcher', telegram_config.model_dump())

    @property
    def all(self):
        return [
            self.db,
            self.dispatcher,
        ]


telegram_lifespans = TelegramLifespans()
