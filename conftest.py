import allure
import pytest
from selenium import webdriver
from pytest_ui_api_template.api.YandexSearchAPI import YandexSearchAPI
from pytest_ui_api_template.utils.config_reader import (get_ui_auth_config,
                                                        get_api_config)


@pytest.fixture(scope="session")
@allure.title("Открытие и закрытие браузера")
def browser():
    with allure.step("Открыть и настроить браузер"):
        driver = webdriver.Chrome()
        driver.maximize_window()
        yield driver

    with allure.step("Закрыть браузер"):
        driver.quit()


@pytest.fixture(scope="session")
@allure.title("Конфиг для UI-авторизации")
def ui_auth_config():
    return get_ui_auth_config()


@pytest.fixture(scope="session")
@allure.title("API-клиент поиска магазинов")
def yandex_api():
    config = get_api_config()
    return YandexSearchAPI(base_url=config["base_url"])
