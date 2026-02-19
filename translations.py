import logging
import subprocess
import sys
from pathlib import Path

from source.core.constants import Language

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# --- Configuration ---
# Add directories or specific .py files to this list
SOURCES = ["source", ".venv/Lib/site-packages/qextrawidgets"]

# Separate directories for source (.ts) and compiled (.qm) translation files
TS_DIR = Path("translations/generated")
QM_DIR = Path("translations/build")

LANGUAGES = list(Language)


def get_python_files():
    """Finds all .py files recursively in directories or adds files directly."""
    files = set()  # Using a set prevents duplicate files

    for src in SOURCES:
        p = Path(src)
        if p.is_dir():
            for py_file in p.rglob("*.py"):
                files.add(str(py_file.resolve()))
        elif p.is_file() and p.suffix == ".py":
            files.add(str(p.resolve()))
        else:
            logging.warning(
                f"Source '{src}' is not a valid directory or .py file. Skipping..."
            )

    if not files:
        logging.error("No Python files found in the provided sources!")
        sys.exit(1)

    return list(files)


def update_translations():
    """Runs pyside6-lupdate to extract strings into .ts files."""
    logging.info("Starting translation updates (.ts)...")
    py_files = get_python_files()

    # Ensures the source translations directory exists
    TS_DIR.mkdir(parents=True, exist_ok=True)

    for lang in LANGUAGES:
        ts_file = TS_DIR / f"{lang}.ts"
        logging.info(f"Processing language: {lang}...")

        command = [
            "pyside6-lupdate",
            *py_files,
            "-ts",
            str(ts_file.resolve()),
            "-no-obsolete",
        ]

        try:
            # capture_output prevents default lupdate messages from polluting your log
            subprocess.run(command, check=True, capture_output=True, text=True)
            logging.info(f"Successfully updated file: {ts_file.name}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running lupdate for {lang}.\nDetails: {e.stderr}")


def build_translations():
    """Runs pyside6-lrelease to compile .ts files into .qm."""
    logging.info("Starting translation compilation (.qm)...")

    # Ensures the compiled translations directory exists
    QM_DIR.mkdir(parents=True, exist_ok=True)

    for lang in LANGUAGES:
        ts_file = TS_DIR / f"{lang}.ts"
        qm_file = QM_DIR / f"{lang}.qm"

        if not ts_file.exists():
            logging.warning(
                f"Source file {ts_file.name} does not exist. Run 'update' first. Skipping..."
            )
            continue

        logging.info(f"Compiling language: {lang}...")
        command = [
            "pyside6-lrelease",
            str(ts_file.resolve()),
            "-qm",
            str(qm_file.resolve()),
        ]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            logging.info(
                f"Successfully compiled file: {qm_file.name} into {QM_DIR.name}/"
            )
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running lrelease for {lang}.\nDetails: {e.stderr}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error(
            "Incorrect usage. Example: python update_translations.py [update|build]"
        )
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == "update":
        update_translations()
    elif action == "build":
        build_translations()
    else:
        logging.error(f"Unknown command: '{action}'")
        logging.info("Available commands: update, build")
        sys.exit(1)
