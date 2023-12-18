#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random
import time
import pyautogui
from webbrowser import open_new_tab
from datetime import datetime
from logging import Logger

from selenium.webdriver import Chrome as ChromeDriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchAttributeException

from autotests.exception import InvalidExpectedConditions
from autotests.exception import InvalidSelectType
from autotests.exception import RedirectionFailedException
from autotests.exception import TimeOutElementNotFoundException
from autotests.exception import UnexpectedBehaviorException
from autotests.exception import NoSuchOptionInTheListException
from autotests.exception import UnexpectedElementTextException
from autotests.exception import UnexpectedAttributeTextException
from autotests.exception import WrongArgumentUsageException


class WebBrowser:

    def __init__(self, driver: ChromeDriver, logger: Logger):
        """
        :param driver: instance of the class selenium.webdriver
        :type driver: object
        :param logger: instance of the class Logger
        :type logger: object
        """

        self.driver = driver
        self.logger = logger

        self.select_type: dict = {
            'css': By.CSS_SELECTOR,
            'xpath': By.XPATH,
            'class_name': By.CLASS_NAME,
            'tag_name': By.TAG_NAME,
            'id': By.ID,
            'name': By.NAME,
            'link text': By.LINK_TEXT,
            'partial link text': By.PARTIAL_LINK_TEXT
        }

        self.conditions: dict = {
            'element_to_be_clickable': EC.element_to_be_clickable,
            'presence_of_element_located': EC.presence_of_element_located,
            'invisibility_of_element_located': EC.invisibility_of_element_located,
            'frame_to_be_available_and_switch_to_it': EC.frame_to_be_available_and_switch_to_it,
            'visibility_of_all_elements_located': EC.visibility_of_all_elements_located
        }

    def close_tab(self):
        pyautogui.hotkey('ctrl', 'w')


    def open_in_new_tab(self, url: str):
        open_new_tab(url)


    def chek_element(self, select_by, locator):
        return EC.element_to_be_clickable((self.select_type[select_by], locator))


    def search_element(self, condition: str, select_by: str, locator: str, description: str,
                       verbose: bool = True, timeout: int = 30):
        """
        Search for a web element
        :param condition: select type of web element waiting in self.conditions
        :type condition: str
        :param select_by: select supported locator in dictionary self.select_by
        :type select_by: str
        :param locator: path to element or identifier in DOM
        :type locator: str
        :param description: a brief description of the web element you are looking for
        :type description: str
        :param verbose: a flag that allows you to write/not write 'description' to a log file
        :type verbose: bool
        :param timeout: waiting time for a web element search
        :type timeout: int

        :return: object WebElement and log entry about successful search_element operation
        """
        wait = WebDriverWait(self.driver, timeout)

        try:
            expected_condition = self.conditions[condition]
        except KeyError:
            message = f'Invalid condition - "{condition}" || ' \
                      f'supported conditions - {list(self.conditions.keys())}'
            self.logger.critical(message)
            raise InvalidExpectedConditions(message)

        try:
            locator_type = self.select_type[select_by]
        except KeyError:
            message = f'Invalid type locator - "{condition}" || ' \
                      f'supported type - {list(self.select_type.keys())}'
            raise InvalidSelectType(message)
        start_time = time.time()

        while True:
            current_time = time.time()

            if current_time - start_time > timeout:
                message = f'Timed out, failed to find on "{description}"'
                if verbose:
                    self.logger.critical(message)
                raise TimeOutElementNotFoundException(message)

            try:
                element = wait.until(expected_condition((locator_type, locator)))
            except StaleElementReferenceException as error:
                self.logger.warning(
                    f'caught {error}, trying to refresh the page and search for element again')
                continue
            except (TimeoutException, NoSuchElementException) as error:
                if expected_condition == EC.frame_to_be_available_and_switch_to_it:
                    message = f'failed to find frame and switched to it, caught {type(error)}. ' \
                              f'Search condition was {expected_condition}'
                elif expected_condition == EC.invisibility_of_element_located:
                    message = f'failed to find element {description} has become invisible, caught {type(error)}. ' \
                              f'Search condition was {expected_condition}'
                else:
                    message = f'failed to find {description}, caught {type(error)}. ' \
                              f'Search condition was {expected_condition}'

                if verbose:
                    self.logger.critical(message)

                raise NoSuchElementException(message)
            else:
                if verbose:
                    if expected_condition == EC.frame_to_be_available_and_switch_to_it:
                        self.logger.info(f'found frame and switched to it')
                    elif expected_condition == EC.invisibility_of_element_located:
                        self.logger.info(f'element {description} has become invisible')
                    else:
                        self.logger.info(f'found {description}')

                return element

    def click_on_element(self, select_by: str, locator: str, description: str, verbose: bool = True, timeout: int = 30):
        """
        Clicking on web elements
        :param select_by: select supported locator type in dictionary self.select_type
        :type select_by: str
        :param locator: path to element or identifier in DOM
        :type locator: str
        :param description: a brief description of the web element to click on
        :type description: str
        :param verbose: a flag that allows you to write/not write 'description' to a log file
        :type verbose: bool
        :param timeout: waiting time for clicking on web element
        :type timeout: int

        :return: object WebElement and log entry about successful click_on_element operation
        """
        wait = WebDriverWait(self.driver, timeout)
        start_time = time.time()

        while True:
            current_time = time.time()

            if current_time - start_time > timeout:
                message = f'Timed out, failed to click on {description}'
                if verbose:
                    self.logger.critical(message)
                raise TimeOutElementNotFoundException(message)

            try:
                wait.until(EC.element_to_be_clickable((self.select_type[select_by], locator))).click()
            except StaleElementReferenceException as error:
                self.logger.warning(
                    f'caught {error}, trying to refresh the page and click on element again')
                continue
            except (TimeoutException, NoSuchElementException) as error:
                message = f'failed to click on {description}, caught error: {type(error)}'
                if verbose:
                    self.logger.critical(message)
                raise NoSuchElementException(message)
            except ElementClickInterceptedException as error:
                self.logger.warning(
                    f'failed to click on {description}, caught error: {error}')
                time.sleep(1)
            else:
                return self.logger.info(f'clicked on {description}')

    def send_keys(
            self,
            select_by: str,
            locator: str,
            description: str,
            value: str = None,
            file: str = None,
            files: list[str | os.PathLike] = None,
            verbose: bool = True,
            timeout: int = 30,
            like_human: bool = False,
            check_value: bool = True,
            clear_field: bool = True
    ):
        """
        Sending text to clickable element, clearing certain text field or uploading file(s).
        Do not use arguments "value", "file" and "files" at the same time, choose only one of them.

        :param select_by: select supported locator type in dictionary self.select_type
        :type select_by: str
        :param locator: path to element or identifier in DOM
        :type locator: str
        :param description: element description for log entry
        :type description: str
        :param value: text that will be sent to input. If value is empty string (value = ""), field will be cleared
        :type value: str
        :param file: filename that will be uploaded
        :type file: str
        :param files: list of files for multiple upload
        :param verbose: True if you want to log messages
        :type verbose: bool
        :param timeout: timeout for element search and sending text to it
        :type timeout: int
        :param like_human: types fast when False, type with random delays between symbols when True
        :type like_human: bool
        :param check_value: checks the entered value with the element's <input value>
        :type check_value: bool
        :param clear_field: clears field before sending keys by default
        :return: log entry about successful send_keys operation
        """
        wait = WebDriverWait(self.driver, timeout)
        start_time = time.time()

        while True:
            current_time = time.time()

            if current_time - start_time > timeout:
                message = f'Timed out, failed to send "{value}" to {description}'
                if verbose:
                    self.logger.critical(message)
                raise TimeOutElementNotFoundException(message)

            try:
                action = ActionChains(self.driver)
                element = """self.search_element(condition='presence_of_element_located',
                                                select_by=select_by,
                                                locator=locator,
                                                description=description,
                                                verbose=False)"""

                if value is not None:
                    value = str(value)

                    if value == '' and not clear_field:
                        message = 'expected either:' \
                                  '1) value == "" and clear_field (clears field and sends nothing),' \
                                  '2) value != "" and clear_field (clears field and sends something),' \
                                  '3) value != "" and not clear field (doesn\'t clear field and sends something)'
                        raise WrongArgumentUsageException(message, self.logger)

                    if clear_field:
                        action.click(eval(element)).pause(0.1)\
                            .key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)\
                            .key_down(Keys.CONTROL).send_keys('x').key_up(Keys.CONTROL)\
                            .pause(0.1).perform()

                        self.logger.info(f'cleared text field "{description}"')

                    if value == '':
                        return

                    if like_human:
                        for symbol in list(value):
                            eval(element).send_keys(symbol)
                            time.sleep(random.uniform(0.05, 0.1))
                    else:
                        eval(element).send_keys(value)

                    if check_value:
                        """found element with props value"""
                        wait.until(lambda _: eval(element, {'self': self,
                                                            'select_by': select_by,
                                                            'locator': locator,
                                                            'description': description,
                                                            'verbose': False}).get_property('value') == value)
                elif file:
                    filepath = os.path.join(os.getcwd(), file)
                    eval(element).send_keys(filepath)
                elif files:
                    abs_filepath_list = [os.path.join(os.getcwd(), item) for item in files]
                    multiple_filepath = ' \n '.join(abs_filepath_list)
                    eval(element).send_keys(multiple_filepath)
                else:
                    message = 'Expected either "value" or "file" argument to be not None'
                    raise WrongArgumentUsageException(message, self.logger)

            except (StaleElementReferenceException, NoSuchElementException) as error:
                self.logger.warning(f'caught {error}, trying to find element and perform send_keys once again')
                continue
            except ElementNotInteractableException as error:
                self.logger.critical(error)
                raise ElementNotInteractableException(error)
            except TimeoutException as error:
                message = f'failed to send keys to element {description}, caught error: {type(error)}'
                if verbose:
                    self.logger.critical(message)
                # raise NoSuchElementException(message)
            except FileNotFoundError as e:
                message = f'no such file or directory "{e}", check your paths'
                raise FileNotFoundError(message)

            else:
                if value:
                    return self.logger.info(f'sent "{value}" to {description}')
                if file:
                    return self.logger.info(f'uploaded "{file}" to {description}')
                if files:
                    return self.logger.info(f'uploaded "{files}" to {description}')

    def check_attribute(self, select_by: str, locator: str, attribute_name: str, text: str = None, timeout: int = 30):
        """
        Checking the attribute of the found web element
        :param select_by: select supported locator type in self.select_type
        :type select_by: str
        :param locator: path to element or identifier in DOM
        :type locator: str
        :param attribute_name: attribute name of the found web element
        :type attribute_name: str
        :param text: text to compare content of the web element attribute with
        :type text: str
        :param timeout: waiting time for double-click a web element
        :type timeout: int
        :return: log entry about successful check_attribute operation.
                 If text="", returns web element attribute text
        """
        start_time = time.time()

        while True:
            current_time = time.time()
            message = f'Timed out, failed to check attribute "{attribute_name}"'

            if current_time - start_time > timeout:
                self.logger.critical(message)
                raise TimeOutElementNotFoundException(message)

            try:
                attribute = self.search_element(condition='presence_of_element_located',
                                                select_by=select_by,
                                                locator=locator,
                                                description=f'found element',
                                                verbose=False).get_attribute(attribute_name)
            except NoSuchAttributeException:
                message = f'failed to find attribute "{attribute_name}" for element "{locator}"'
                self.logger.critical(message)
                raise NoSuchAttributeException(message)
            except StaleElementReferenceException as error:
                self.logger.warning(f'caught {error}, trying to find element and check its attribute once again')
                continue
            except (TimeoutException, NoSuchElementException) as error:
                message = f'failed to check attribute, caught error: {type(error)}'
                self.logger.critical(message)
                raise NoSuchElementException(message)
            else:
                if text:
                    if text in attribute:
                        return self.logger.info(f'found "{text}" in attribute "{attribute_name}" text')

                    message = f'failed to find "{text}" in attribute "{attribute_name}" - ' \
                              f'expected "{text}", got "{attribute}"'
                    raise UnexpectedAttributeTextException(message, self.logger)
                else:
                    self.logger.info(f'checked "{attribute_name}" attribute: {attribute}')
                    return attribute


    def check_text(self, select_by: str, locator: str, description: str, text: str = None, timeout: int = 30):
        """
        Checking text in web element
        :param select_by: select supported locator type in self.select_type
        :type select_by: str
        :param locator: path to element or identifier in DOM
        :type locator: str
        :param description: element description for log entry
        :type description: str
        :param text: text for checking
        :type :str
        :param timeout: waiting time for search a web element
        :type : int
        :return: log entry about successful check_text operation. Returns web element text, if text argument is None.
        """
        start_time = time.time()

        while True:
            current_time = time.time()
            message = f'Timed out, failed to check text of {description}'

            if current_time - start_time > timeout:
                self.logger.critical(message)
                raise TimeOutElementNotFoundException(message)

            try:
                element_text = self.search_element(condition='presence_of_element_located',
                                                   select_by=select_by,
                                                   locator=locator,
                                                   description=f'found element',
                                                   verbose=False).text
            except StaleElementReferenceException as e:
                self.logger.warning(f'caught {e}, trying to find and check page header once again')
                continue
            except Exception:
                message = 'failed to find element text'
                raise UnexpectedBehaviorException(message, self.logger)
            else:
                if text:
                    if element_text == text:
                        return self.logger.info(f'{description} text is equal to expected "{text}"')
                    else:
                        message = f'{description} text "{element_text}" differs from expected "{text}"'
                        raise UnexpectedElementTextException(message, self.logger)
                else:
                    self.logger.info(f'from web-element extracted text "{element_text}"')
                    return element_text
