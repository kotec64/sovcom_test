from pytest_bdd import when, then, parsers, given
from autotests.exception import TimeOutElementNotFoundException


def check_field_name(field_name):
    if field_name == 'Эллектроннная почта или телефон':
        locator = 'username'
    if field_name == 'Пароль':
        locator = 'userpassword'
    return locator


def send_values(selenium_client, locator, value):
    selenium_client.send_keys(
        select_by='id',
        locator=locator,
        value=value,
        description='search by key_word')


@given(parsers.parse('Open the "{key}" page'))
def get_url(selenium_client, browser, logger, key, params):
    params['key'] = 'https://www.pochta.ru'
    browser.get(params['key'])


@when(parsers.parse('click to "{key}"'))
@given(parsers.parse('click to "{key}"'))
@then(parsers.parse('click to "{key}"'))
def click_to_element(selenium_client, key, params):
    selenium_client.click_on_element(
        select_by='xpath',
        locator=f'//*[starts-with(text(),"{key}")]',
        timeout=5,
        description=f'"{key}"'
    )
    params['button_name'] = key

@given(parsers.parse('get placeholder by id "{id}"'))
def get_placeholder(selenium_client, logger, id, params):
    if id == 'countryTo':
        locator = "//div[@id= 'countryTo']//child::input"
        select_by = 'xpath'
    else:
        locator = id
        select_by = 'id'
    placeholder = selenium_client.check_attribute(select_by=select_by,
                                    locator=locator,
                                    attribute_name='placeholder'

    )
    button_name = params['button_name']
    if not 'placeholders' in params:
        params['placeholders'] = {button_name:placeholder}
    else:
        params['placeholders'][button_name] = placeholder

@then(parsers.parse('Check that the field "{field_name}" is empty'))
def check_field(selenium_client, logger, field_name, params):
    locator = check_field_name(field_name)
    selenium_client.check_text(select_by='id',
                               locator=locator,
                               description=f'username')


@when(parsers.parse('Enter "{value}" in the “{field_name}” field'))
def send_keys_to_field(selenium_client, logger, value, field_name, params):
    locator = check_field_name(field_name)
    if value == '    ':
        try:
            send_values(selenium_client, locator, value)
        except: TimeOutElementNotFoundException

        else:
            message = 'we can send any space to field'
            raise ValueError(message)
    else:
        send_values(selenium_client, locator, value)


@then('Print validation message')
def get_and_print_message(selenium_client, logger, params):
    element_text = selenium_client.search_element(condition='presence_of_element_located',
                                                  select_by='xpath',
                                                  locator="//div[@id = 'usernameError']//child::span",
                                                  description=f'found element',
                                                  verbose=False).text
    logger.info(f'element_text - {element_text}')
    print(f'element_text - {element_text}')