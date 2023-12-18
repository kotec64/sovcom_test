import os
import pytest
from datetime import datetime
import logging
from typing import Any

from autotests.selenium_functions import WebBrowser
from autotests.exception import UnexpectedBehaviorException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Chrome as ChromeDriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

PATH_TO_DRIVER = ChromeDriverManager().install()


@pytest.fixture
def selenium_client(browser: ChromeDriver, logger: logging.Logger) -> WebBrowser:
    """
    :param browser: instance of the class
    :type browser: ChromeDriver
    :param logger: instance of the class
    :type logger: Logger
    :return: instance of the class
    :rtype: WebBrowser
    """
    browser_client = WebBrowser(browser, logger)
    return browser_client


@pytest.fixture
def browser(params: dict, request: object, logger: logging.Logger) -> ChromeDriver:
    """
    :param params: dictionary with data (fixture)
    :type params: dict
    :param request: request fixture is a special fixture providing information of the requesting test function
    :type request: object
    :param logger: instance of the class Logger
    :type logger: object
    """

    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--force-device-scale-factor=1")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(executable_path=PATH_TO_DRIVER)

    timeout = 300
    start_time = datetime.now()
    current_time = datetime.now()
    tries = 0
    while (current_time - start_time).total_seconds() <= timeout:
        try:
            driver = ChromeDriver(service=service, options=options)
            break
        except WebDriverException as e:
            logger.warning(f"Failed to start Chrome due to {e}. Trying again...")
            tries += 1
            current_time = datetime.now()
            continue
    else:
        message = f"Failed to start Chrome after {tries} tries. "
        raise UnexpectedBehaviorException(message, logger)

    driver.maximize_window()

    driver.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )

    download_dir = os.path.join(os.getcwd(), "test_download")
    download_params = {
        "cmd": "Page.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": download_dir},
    }
    driver.execute("send_command", download_params)

    yield driver
    driver.close()
    driver.quit()


@pytest.fixture(scope='session')
def params():
    dict = {}
    yield dict


@pytest.fixture
def logger(request: Any) -> logging.Logger:
    """
    :param request: request fixture is a special fixture providing information of the requesting test function
    :return: instance of the class Logger
    """
    logfile = os.path.join(
        "logs",
        f'{request.node.originalname}-{datetime.today().strftime("%Y-%m-%d_%H_%M_%S_%f")}.log',
    )
    # make sure that folder for logs exists:
    if not os.path.exists(os.path.normpath("./logs")):
        os.makedirs("logs")

    logger = logging.getLogger(logfile)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("| %(asctime)s | %(levelname)s | %(message)s")
    formatter.default_msec_format = "%s.%03d"
    fh = logging.FileHandler(logfile, encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger