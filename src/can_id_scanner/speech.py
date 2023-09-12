"""Text-to-speech module."""

import queue
import sys
import tempfile
import threading
from pathlib import Path

import gtts
import playsound

from can_id_scanner import browser
from can_id_scanner.common import ROOT_DIR
from can_id_scanner.common import logger


def get_resource(relative: str):
    """Get a resource file."""
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative
    return ROOT_DIR / "resources" / relative


class Speaker(threading.Thread):
    """Text-to-speech thread."""

    queue: queue.Queue

    def __init__(self):
        """Initialize the speech thread."""
        super().__init__(name="Speech Thread", daemon=True)
        self.queue = queue.Queue()

    def say(self, text):
        """Say something."""
        self.queue.put(text)

    def stop(self):
        """Stop the speech thread."""
        self.queue.put(None)
        self.join()

    def run(self):
        """Run the speech thread."""
        # initialize on same thread
        while True:
            job = self.queue.get()
            if job is None:
                break

            try:
                self._process_job(job)
            except Exception as e:
                logger.opt(exception=e).error("Error processing job:")

    def _process_job(self, job):
        if isinstance(job, str):
            logger.info(f"Saying: {job}")
            with tempfile.NamedTemporaryFile(suffix=".mp3") as f:
                audio = gtts.gTTS(text=job)
                audio.save(f.name)
                playsound.playsound(f.name)
            return

        if isinstance(job, Path):
            logger.info(f"Playing: {job.name}")
            playsound.playsound(str(job))
            return

        raise ValueError(f"Unknown job: {job}")


def greet(speaker: Speaker):
    """Greet a new client."""
    # success ding for a successful scan
    speaker.say(get_resource("success.wav"))


def ready(speaker: Speaker):
    """Indicate that the scanner is ready to scan."""
    speaker.say("Ready for next client.")


def error(speaker: Speaker):
    """Indicate that an error occurred."""
    speaker.say("Need Assistance.")


def on_result(speaker: Speaker, name: str, result: browser.SubmitResult):
    """Indicate the result of submitting a name."""
    if result == browser.SubmitResult.SUCCESS:
        speaker.say(f"Thank you, {name}.")
    elif result == browser.SubmitResult.NEW_CLIENT:
        speaker.say("New client. Need assistance.")
    elif result == browser.SubmitResult.NOT_READY:
        speaker.say("Need assistance.")
    elif result == browser.SubmitResult.MISSING_INFO:
        speaker.say("Need assistance.")
