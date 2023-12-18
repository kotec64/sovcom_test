from autotests.general_steps import *
from pytest_bdd import scenario, then


@scenario('../features/Scenarios.feature',
          'creating a dictionary with button data')
def test_live_broadcast_load_page():
    print('creating a dictionary with button data test passed')


@then('print the resulting dictionary')
def search_by_key_word(selenium_client, logger, params):
    print(f"placeholders = {params['placeholders']}")
    logger.info(f"placeholders = {params['placeholders']}")
