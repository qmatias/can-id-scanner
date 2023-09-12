"""Module for interacting with the link2feed portal page."""
import enum
import time

from loguru import logger
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class SubmitResult(enum.Enum):
    """Result of submitting a name to the link2feed portal."""

    SUCCESS = enum.auto()
    """The name was successfully submitted."""

    NOT_READY = enum.auto()
    """Need to navigate to the portal page first."""

    NEW_CLIENT = enum.auto()
    """The name was submitted, but it was a novel client."""

    MISSING_INFO = enum.auto()
    """The name was submitted, but it was missing information."""


class BrowserSettings(BaseSettings):
    """Settings for the link2feed portal page."""

    org: str

    login_user: str
    login_pass: str

    base_url: str = "https://portal.link2feed.com"
    login_url: str = "https://accounts.link2feed.com/users/sign_in"

    @property
    def org_url(self):
        """The URL for the organization page."""
        return self.base_url + "/org/" + self.org

    @property
    def portal_url(self):
        """The URL for the portal page."""
        return self.org_url + "/dashboard"

    model_config = SettingsConfigDict(env_prefix="scanner_")


def setup_driver(browser_settings: BrowserSettings):
    """Setup the selenium webdriver."""
    driver = webdriver.Chrome()
    driver.implicitly_wait(1)
    driver.get(browser_settings.login_url)
    driver.find_element(By.ID, "user_email").send_keys(browser_settings.login_user)
    driver.find_element(By.ID, "user_password").send_keys(browser_settings.login_pass)
    driver.find_element(By.NAME, "commit").click()
    time.sleep(1)
    driver.get(browser_settings.portal_url)
    return driver


def submit_name(driver, browser_settings: BrowserSettings, name: str):
    """Attempt to submit name to the link2feed portal."""
    if driver.current_url not in (
        browser_settings.portal_url,
        browser_settings.org_url,
    ):
        logger.warning("Detected barcode, but not on portal page. Skipping.")
        return SubmitResult.NOT_READY

    # enter name into searchbox
    search_box = driver.find_element(By.ID, "intake_search_client_search_handler")
    search_box.clear()
    search_box.send_keys(name)
    time.sleep(1)  # allow results to load

    # load results, select first result
    search_results = driver.find_element(By.ID, "ui-id-3")
    try:
        first_result = search_results.find_element(
            By.CLASS_NAME, "ui-menu-item"
        ).find_element(By.TAG_NAME, "a")
    except NoSuchElementException:
        # no results found
        logger.warning(f"No results found for {name}. Aborting.")
        return SubmitResult.NEW_CLIENT
    first_result.click()

    # on user page, navigate to services page
    service_btn = driver.find_element(By.XPATH, "//span[contains(text(), 'SERVICES')]")

    # find parent li element -- it has the class 'completed' if the user has
    # profile is complete and they can receive services
    parent = service_btn.find_element(By.XPATH, "..")
    while parent.tag_name != "li":
        print(parent.tag_name)
        parent = parent.find_element(By.XPATH, "..")

    # check if it's clickable
    if "completed" not in parent.get_attribute("class"):
        logger.warning(f"User account not completed: {name}, aborting.")
        return SubmitResult.MISSING_INFO

    # navigate to services page
    service_btn.click()

    # start new tefap visit
    tefap_visit_btn = driver.find_element(
        By.XPATH, "//*[contains(text(), 'New TEFAP Pantry Visit')]"
    )
    tefap_visit_btn.click()

    # select visit reason checkbox
    visit_checkbox = driver.find_element(By.ID, "form-visit-reason-11538")
    checkbox_clickable = visit_checkbox.find_element(By.XPATH, "..").find_element(
        By.TAG_NAME, "span"
    )
    checkbox_clickable.click()
    time.sleep(0.5)  # the checkbox takes a moment to update

    # submit form
    form = driver.find_element(By.ID, "form-program-visit")
    form.submit()

    # navigate back to dashboard
    time.sleep(1)
    driver.get(browser_settings.portal_url)

    logger.info(f"Succesfully processed user: {name}.")
    return SubmitResult.SUCCESS
