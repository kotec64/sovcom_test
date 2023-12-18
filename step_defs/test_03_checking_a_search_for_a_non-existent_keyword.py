from autotests.general_steps import *
from pytest_bdd import scenario, when, then, parsers


@scenario('../features/Scenarios.feature',
          'checking a search for a non-existent keyword')
def test_live_broadcast_load_page():
    print('checking a search for a non-existent keyword test passed')


@when(parsers.parse('search the site with the word “{key_word}”'))
def open_the_page(params, browser, key_word, selenium_client, logger):
    selenium_client.click_on_element(
        select_by='xpath',
        locator='//*[@role = "button"]',
        timeout=5,
        description='"search"'
    )
    selenium_client.send_keys(
        select_by='xpath',
        locator='//input[@placeholder = "Поиск по сайту"]',
        value=key_word,
        description='search by key_word'
    )
    selenium_client.click_on_element(
        select_by='xpath',
        locator='//*[@data-testid = "search-button"]',
        timeout=5,
        description='"search"'
    )


@then(parsers.parse('The search results match the {expected_result}'))
def search_by_key_word(selenium_client, logger, expected_result, params):
    locator = '//*[@data-component = "NotificationWrapper"]//child::div[2]//child::div'
    selenium_client.check_text(select_by='xpath',
                               locator=locator,
                               text=expected_result,
                               description=f'username')
