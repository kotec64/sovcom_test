from autotests.general_steps import *
from pytest_bdd import scenario, given, then, parsers
from selenium.common.exceptions import NoSuchElementException


@scenario('../features/Scenarios.feature',
          'incorrect login')
def test_live_broadcast_load_page():
    print('incorrect login test passed')


@given('click to "Войти" with js')
def open_the_page(params, browser, selenium_client):
    elem = selenium_client.search_element(condition='presence_of_element_located',
                                          select_by='xpath',
                                          locator="//a[starts-with(text(),'Войти')]",
                                          description=f'found element',
                                          verbose=False)
    browser.execute_script("arguments[0].click();", elem)



@then(parsers.parse('Check that the button "Войти" is not available'))
def search_by_key_word(selenium_client, logger, params):
    try:
        selenium_client.click_on_element(
            select_by='xpath',
            locator=f"//span[starts-with(text(),'Войти')]//ancestor::button",
            timeout=5,
            description=f'"Почта России"'
        )
    except: NoSuchElementException

    else:
        message = 'button is enable'
        raise ValueError(message)
