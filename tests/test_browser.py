"""Test the browser module."""

import pytest

from can_id_scanner.browser import BrowserSettings
from can_id_scanner.browser import setup_driver
from can_id_scanner.browser import submit_name


@pytest.fixture
def browser_settings():
    return BrowserSettings(  # noqa: S106
        org="16731",
        login_user="fnabilsi@canwashtenaw.org",
        login_pass="Malik2008#",
    )


@pytest.fixture
def driver(browser_settings):
    driver = setup_driver(browser_settings)
    yield driver
    driver.quit()


@pytest.mark.parametrize(
    "name",
    [
        "Matias Kotlik",
        "Sunny Liu",
    ],
)
def test_browser(driver, browser_settings, name):
    submit_name(driver, browser_settings, name)
    assert driver.current_url == browser_settings.portal_url
