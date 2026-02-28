from time import sleep

import pytest
import allure
from pytest_ui_api_template.pages.AuthPage import AuthPage
from pytest_ui_api_template.pages.HomePage import HomePage
from pytest_ui_api_template.pages.SearchPage import SearchPage


@pytest.mark.ui
@allure.parent_suite("UI-тесты")
@allure.suite("Авторизация в Яндекс ID")
@allure.title("Авторизация до шага 'Безопасный вход'")
@allure.description(
    "Открываем страницу авторизации, выбираем вход по логину, "
    "вводим логин и пароль, решаем капчу вручную и "
    "проверяем, что открылся шаг «Безопасный вход»."
)
@allure.feature("Авторизация")
@allure.severity(allure.severity_level.CRITICAL)
def test_auth(browser, ui_auth_config):
    """
    Авторизация пользователя до шага 'Безопасный вход'
    """
    auth_page = AuthPage(
        driver=browser,
        ui_auth_url=ui_auth_config["ui_auth_url"])
    with allure.step("Открыть страницу авторизации"):
        auth_page.go()
    with allure.step("Нажать на кнопку 'Войти' на старотом экране"):
        auth_page.submit()
    with allure.step("Выбрать вход по логину"):
        auth_page.add_else()
        auth_page.click_login_by()
    with allure.step("Ввести логин пользователя"):
        auth_page.add_login(ui_auth_config["login"])
    with allure.step("Нажать 'Войти' после ввода логина"):
        auth_page.submit()
    with allure.step("Ввести пароль пользователя"):
        auth_page.add_password(ui_auth_config["password"])
    with allure.step("Нажать 'Далее' на шаге пароля"):
        auth_page.click_password_next()
    with allure.step("Решить капчу вручную и продолжить тест"):
        input("РЕШИ КАПЧУ ВРУЧНУЮ И НАЖМИ ENTER В КОНСОЛИ → ")
    with allure.step("Проверить что открыт шаг 'Безопасный вход'"):
        assert auth_page.is_on_secure_login_step()


@pytest.mark.ui
@allure.parent_suite("UI-тесты")
@allure.suite("Оформление заказа без авторизации")
@allure.title("Переход на экран логина при оформлении без авторизации")
@allure.description(
    "Открываем главную страницу доставки, подтверждаем адресс, "
    "заходим в магазин 'Магнит', добавляем товар в корзину и "
    "переходим к оформлению. Ожидаем, что неавторизованный пользователь"
    "будет перенаправлен на экран логина"
)
@allure.feature("Авторизация")
@allure.severity(allure.severity_level.CRITICAL)
def test_home(browser, ui_auth_config):
    """
    Добавление товара и переход к оформлению для
    неавторизованного пользователя.
    Ожидаем переход на экран логина.
    """
    home_page = HomePage(
        driver=browser,
        ui_url=ui_auth_config["ui_url"]
    )
    auth_page = AuthPage(
        driver=browser,
        ui_auth_url=ui_auth_config["ui_auth_url"]
    )

    with allure.step("Переход на главную страницу"):
        home_page.go()
    with allure.step("Подтверждение адресса доставки"):
        home_page.confirm_address()
    with allure.step("Переход в магазин 'Магнит'"):
        home_page.go_to_magnit_store()
    with allure.step(
            "Выбор товара 'Напиток Evervess Cola газированный'"
    ):
        home_page.select_product()
    with allure.step("Добавление товара в корзину"):
        home_page.add_product_to_cart()
    with allure.step("Переход к оформлению заказа"):
        home_page.proceed_to_checkout()
    with allure.step("Проверка перехода на экран логина"):
        assert auth_page.is_login_page_opened()


@pytest.mark.ui
@allure.parent_suite("UI-тесты")
@allure.suite("Поиск товара по наванию")
@allure.title("Поиск товара 'Мороженое' по названию")
@allure.description(
    "Открываем главную страницу доставки переходим к поиску, "
    "вводим товар 'Мороженое', нажимаем кнопку 'Найти' и"
    "проверям, что товар присутствует в результатах поиска."
)
@allure.feature("Поиск товара")
@allure.severity(allure.severity_level.CRITICAL)
def test_search(browser, ui_auth_config):
    """
    Поиск товара по названию
    """
    search_page = SearchPage(
        driver=browser,
        ui_url=ui_auth_config["ui_url"]
    )
    with allure.step("Переход на главную страницу"):
        search_page.go()
    with allure.step("Вввод текста 'Мороженное' в поле поиска"):
        search_page.search_product("Мороженое")
    with allure.step("Нажимает кнопку 'Найти'"):
        search_page.submit_search()
    with allure.step(
            "Проверить, что товар 'Мороженое' найден в результатах поиска"
    ):
        assert search_page.has_product_in_results("Мороженое")


@pytest.mark.ui
@allure.parent_suite("UI-тесты")
@allure.suite("Поиск товара по наванию")
@allure.title("Негативеый поиск товара по неккоректному запросу")
@allure.description(
    "Открываем главную страницу доставки переходим к поиску, "
    "вводим неккоректный запрос 'qweqwe123!@#', нажимаем кнопку 'Найти' и"
    "проверям, что отображается экран с текстом 'Ничего не нашли, но есть:'."
)
@allure.feature("Поиск товара")
@allure.severity(allure.severity_level.NORMAL)
def test_search_no_results(browser, ui_auth_config):
    """
    Негативный поиск по неккоректному запросу.
    """
    search_page = SearchPage(
        driver=browser,
        ui_url=ui_auth_config["ui_url"]
    )
    with allure.step("Переход на главную страницу поиска"):
        search_page.go()
    with allure.step(
            "Ввод неккоректного запроса 'qweqwe123!@#' и запуск поиска"
    ):
        search_page.search_product("qweqwe123!@#").submit_search()
    with allure.step(
            "Проверить, что отображается экран 'Ничего не нашли, но есть'"
    ):
        assert search_page.is_not_result_message_visible()


@pytest.mark.ui
@allure.parent_suite("UI-тесты")
@allure.suite("Поиск заведения по наванию")
@allure.title("Переход в карточку заведения из результатов поиска")
@allure.description(
    "Открываем главную страницу доставки, переходим к поиску, "
    "вводим название заведения  'Burger King', нажимаем кнопку 'Найти' и"
    "переходим в карточку первого заведения из результатов."
    "Проверям, что заголовок карточки совпадает с названием в выдаче."
)
@allure.feature("Поиск заведения")
@allure.severity(allure.severity_level.NORMAL)
def test_open_place_from_search(browser, ui_auth_config):
    """
    Переход из результатов поиска в карточку заведения.
    """
    search_page = SearchPage(
        driver=browser,
        ui_url=ui_auth_config["ui_url"]
    )
    with allure.step("Переход на главную страницу поиска"):
        search_page.go()
    with allure.step("Вввод текста 'Burger King' в поле поиска"):
        search_page.search_product("Burger King").submit_search()
    with allure.step("Открыть первое заведение из результатов поиска"):
        search_page.open_first_place()
    with allure.step(
            "Проверить, что открыта карточка того же заведения,"
            "которое было выбрано в результатах поиска"
    ):
        assert search_page.is_place_page_opened()
