"""CAN ID Scanner app."""

import cv2
import typer
from rich import print

from can_id_scanner import barcode
from can_id_scanner import browser
from can_id_scanner import speech
from can_id_scanner.common import WINDOW_NAME
from can_id_scanner.common import logger


app = typer.Typer()


@app.command()
@logger.catch
def run_scanner(  # noqa: S107
    org: str = "16731",
    login_user: str = "fnabilsi@canwashtenaw.org",
    login_pass: str = "Malik2008#",  # noqa: S106
    video_device: int = 0,
):
    """Run the CAN ID Scanner app."""
    logger.info("Starting CAN ID Scanner App...")

    browser_settings = browser.BrowserSettings(
        org=org, login_user=login_user, login_pass=login_pass
    )
    driver = browser.setup_driver(browser_settings)
    logger.info("Initialized Webdriver.")

    video = cv2.VideoCapture(video_device)
    logger.info("Initialized video capture.")

    speaker = speech.Speaker()
    speaker.start()

    print("[bold]CAN ID Scanner[/bold]")
    print("Press [bold]Ctrl+C[/bold] to exit.")
    speech.ready(speaker)
    while True:
        _, frame = video.read()
        cv2.imshow(WINDOW_NAME, frame)

        identity = barcode.read_identity(frame)
        if identity:
            speech.greet(speaker)
            try:
                result = browser.submit_name(
                    driver, browser_settings, identity.full_name
                )
            except Exception as e:
                logger.opt(exception=e).error("Error submitting to browser:")
                speech.error(speaker)
            else:
                speech.on_result(speaker, identity.nickname, result)
            speech.ready(speaker)

        cv2.putText(
            frame,
            "Press [q] to exit.",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            1,
        )
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    driver.quit()
    video.release()
    cv2.destroyAllWindows()
    speaker.stop()


if __name__ == "__main__":
    app()
