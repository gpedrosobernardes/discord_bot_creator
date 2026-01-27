import os
from source.controllers.base import BaseController
from source.views.credits import CreditsView


class CreditsController(BaseController[CreditsView]):
    def __init__(self):
        super().__init__(CreditsView())
        self._load_licenses()

    def _load_licenses(self) -> None:
        """Loads the THIRD-PARTY license file and updates the view."""
        # Path relative to this file: source/controllers/credits.py -> ../../THIRD-PARTY
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        file_path = os.path.join(project_root, "THIRD-PARTY")

        # Check for THIRD-PARTY or THIRD-PARTY.txt
        if not os.path.exists(file_path):
            file_path_txt = f"{file_path}.txt"
            if os.path.exists(file_path_txt):
                file_path = file_path_txt
            else:
                self.view.set_licenses("THIRD-PARTY file not found.")
                return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.view.set_licenses(content)
        except OSError as e:
            self.view.set_licenses(f"Error reading license file: {e}")
