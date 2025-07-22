from settings.db import db_config
from web.lifespans.db import db_init


class AppLifespans:
    @property
    def db(self):
        return db_init('db_pool', db_config.model_dump())

    @property
    def all(self):
        return [
            self.db,
        ]


app_lifespans = AppLifespans()
