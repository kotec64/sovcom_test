@project
Feature: test scenarios

  @site_search
  Scenario: site search
    Given get url from file
    And open the page with the received url
    When In the search engine, search for the word "Почта РФ"
    Then Print the number of results found
    And Open in new tab "https://www.pochta.ru"
    And Close the search engine tab

  @negative_login
  Scenario: incorrect login
    Given Open the "Russian Post" page
    And click to "Войти" with js
    When click to "Войти"
    Then Check that the button "Войти" is not available
    And Check that the field "Эллектроннная почта или телефон" is empty
    And Check that the field "Пароль" is empty
    When Enter "    " in the “Эллектроннная почта или телефон” field
    Then Print validation message
    When Enter "qwerty" in the “Эллектроннная почта или телефон” field
    Then Print validation message

  @checking_a_search
  Scenario Outline: checking a search for a non-existent keyword
    Given Open the "Russian Post" page
    When search the site with the word “Совкомбанк”
    Then The search results match the <expected_result>

    Examples:
    | expected_result                                                                                                  |
    | Извините, по вашему запросу “Совкомбанк” ничего не найдено. Попробуйте изменить запрос или вернитесь на главную. |

  @Creating_a_dictionary
  Scenario: creating a dictionary with button data
    Given Open the "Russian Post" page
    And click to "Отправить"
    And click to "Посылку"
    And click to "В другую страну"
    And get placeholder by id "countryTo"
    And click to "По номеру телефона"
    And get placeholder by id "phoneTo"
    And click to "По индексу"
    And get placeholder by id "indexTo"
    And click to "По России"
    And get placeholder by id "addressTo"
    Then print the resulting dictionary


