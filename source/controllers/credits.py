from source.controllers.base import BaseController
from source.views.credits import CreditsView


class CreditsController(BaseController[CreditsView]):
    def __init__(self):
        super().__init__(CreditsView())
