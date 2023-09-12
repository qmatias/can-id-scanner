"""Tests for playing sound."""

import pytest

from can_id_scanner import browser
from can_id_scanner import speech


@pytest.fixture
def speaker():
    speaker = speech.Speaker()
    speaker.start()
    yield speaker
    speaker.stop()


def test_speaker(speaker):
    speech.greet(speaker, "Matias")
    speech.ready(speaker)
    speech.error(speaker)
    speech.on_result(speaker, "Matias", browser.SubmitResult.SUCCESS)
    speech.on_result(speaker, "Matias", browser.SubmitResult.NEW_CLIENT)
    speech.on_result(speaker, "Matias", browser.SubmitResult.NOT_READY)
    speech.on_result(speaker, "Matias", browser.SubmitResult.MISSING_INFO)


def test_greet(speaker):
    speech.greet(speaker)
