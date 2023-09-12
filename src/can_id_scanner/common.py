"""Shared constants and functions for the CAN ID Scanner application."""

from pathlib import Path

import typer
from loguru import logger


ROOT_DIR = Path(__file__).parent.parent.parent

APP_NAME = "CAN ID Scanner"
APP_SLUG = "can-id-scanner"
WINDOW_NAME = f"{APP_NAME} - Camera Feed"

APP_DIR = Path(typer.get_app_dir(APP_NAME))
LOG_DIR = APP_DIR / "logs"

logger.add(
    LOG_DIR / "{time}.log",
    backtrace=True,
    diagnose=True,
    rotation="1 day",
    retention="7 days",
)
