from core.base_app import BaseApplication
from core.bot import Bot


if __name__ == "__main__":
    app = BaseApplication()
    bot = Bot(app.user_settings.value("database"))
    bot.run(app.user_settings.value("token"))
