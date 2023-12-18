import re
from pytest_bdd import scenario, given, when, then, parsers


@scenario('../features/Scenarios.feature',
          'site search')
def test_live_broadcast_load_page():
    print('site search test passed')


@given('get url from file')
def get_url(selenium_client, browser, logger, params):
    file = open('template_files/url.txt')
    params['url'] = file.readlines()
    logger.info(f"url = {params['url']}")


@given('open the page with the received url')
def open_the_page(params, browser):
    browser.get(params['url'][0])


@when(parsers.parse('In the search engine, search for the word "{key_word}"'))
def search_by_key_word(selenium_client, logger, params, key_word):
    selenium_client.send_keys(
        select_by='xpath',
        locator="//textarea[@title = 'Поиск']",
        value=key_word,
        description='search by key_word')

    selenium_client.click_on_element(
        select_by='xpath',
        locator=f'//span[starts-with(text(),"почта рф")]',
        timeout=5,
        description=f'"Почта России"'
    )


@then('Print the number of results found')
def calculating_and_printing_results(selenium_client, logger, params):
    element_text = selenium_client.search_element(condition='presence_of_element_located',
                                                   select_by='id',
                                                   locator='result-stats',
                                                   description=f'found element',
                                                   verbose=False).text
    logger.info(f'element_text - {element_text}')
    element_text_2 = (re.findall(r'[0-9]+|[0-9]', element_text))
    element_text_2.pop(-1)
    element_text_2.pop(-1)

    logger.info('Approximate number of results - ' + ' '.join(element_text_2))
    print('Approximate number of results - ' + ' '.join(element_text_2))


@then(parsers.parse('Open in new tab "{url}"'))
def open_new_tab(selenium_client, params, browser, url, logger):
    params['Russian Post'] = url
    params['handle_search'] = browser.current_window_handle
    selenium_client.open_in_new_tab(url)
    params['handle_post'] = browser.current_window_handle

@then('Close the search engine tab')
def close_tab(selenium_client, params, browser, logger):
    browser.switch_to.window(params['handle_search'])
    selenium_client.close_tab()
