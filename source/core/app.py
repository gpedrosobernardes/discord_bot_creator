import logging
import sys

from source.controllers.config import ConfigController
from source.controllers.credits import CreditsController
from source.controllers.logs import LogsController
from source.controllers.main import MainController
from source.core.base_app import BaseApplication
from source.core.database import DatabaseController
from source.core.log_handler import LogHandler


class Application(BaseApplication):
    def __init__(self):
        super().__init__()
        self.database = DatabaseController(self.user_settings.value("database"), "main")

        self.log_handler = LogHandler(self.database)
        logging.getLogger("core").addHandler(self.log_handler)

        self.config_controller = ConfigController(self.translator, self.user_settings)
        self.logs_controller = LogsController(self.database)
        self.credits_controller = CreditsController()
        self.main_controller = MainController(
            self.database,
            self.user_settings,
            self.config_controller,
            self.logs_controller.view,
            self.credits_controller.view,
            self.log_handler,
        )

        self.setup_connections()
        self.main_controller.load_initial_state()
        sys.exit(self.exec())

    def setup_connections(self):
        for controller in (
            self.config_controller,
            self.main_controller,
            self.logs_controller,
        ):
            self.config_controller.language_changed.connect(controller.translate_ui)

        self.main_controller.switch_project.connect(
            self.logs_controller.load_logs_model
        )
