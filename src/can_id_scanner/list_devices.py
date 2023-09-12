"""List available video devices."""
import time

import cv2
import typer
from rich import print

from can_id_scanner.common import logger


app = typer.Typer()


@app.command()
@logger.catch
def list_devices():
    """List available video devices."""
    i = 0
    while True:
        video = cv2.VideoCapture(i)
        if not video.isOpened():
            break
        print(f"[bold]Device {i}[/bold]: [i]{video.getBackendName()}[/i]")
        video.release()
        i += 1

    print(f"Found [bold]{i}[/bold] video devices.")
    print("Use the [bold]--video-device[/bold] option to select one.")
    print("Press [bold]Ctrl+C[/bold] to exit.")

    while True:
        time.sleep(1)


if __name__ == "__main__":
    app()
