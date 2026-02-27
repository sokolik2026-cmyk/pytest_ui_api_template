import pytest
import allure


@pytest.mark.api
@allure.parent_suite("API-тесты")
@allure.suite("Поиск по запросу")
@allure.feature("Поиск по API")
@allure.story("Поиск магазинов по тексту на кириллице")
@allure.title("Поиск по запросу на кирилице")
@allure.description(
    "Отправляем запрос поиска по тексту 'Магнит Косметик' на кириллице "
    "с корректными координатами. Ожидаем успешный ответ 200 "
    "и непустой список мест."
)
@allure.severity(allure.severity_level.CRITICAL)
def test_search_cyrillic(yandex_api) -> None:
    """
    Поиск по запросу на кириллице
    """
    with allure.step("Отправить запрос поиска по тексту 'Магнит Косметик'"):
        response = yandex_api.search(
            text="Магнит Косметик",
            longitude=39.20625192316922,
            latitude=51.679693589701465,
        )

    with allure.step("Проверить, что статус ответ равен 200"):
        assert response.status_code == 200

    with allure.step("Разобрать тело ответа в JSON"):
        data = response.json()

    with allure.step("Проверить заголовок результата поиска"):
        assert data["header"]["text"].startswith("Найдено")

    with allure.step("Проверить, что блок places не пустой"):
        places_blocks = [b for b in data["blocks"] if b["type"] == "places"]
        assert places_blocks
        places = places_blocks[0]["payload"]
        assert len(places) > 0


@pytest.mark.api
@allure.parent_suite("API-тесты")
@allure.suite("Поиск по запросу")
@allure.feature("Поиск по API")
@allure.story("Поиск магазинов по тексту на латинице")
@allure.title("Поиск по запросу на латинице")
@allure.description("Отправляем запрос поиска по тексту 'fix' на латинице "
    "с корректными координатами. Ожидаем успешный ответ 200 "
    "и непустой список мест.")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_latin(yandex_api) -> None:
    """
    Поиск по запросу на латинице
    """
    with allure.step("Отправить запрос поиска по тексту 'fix'"):
        response = yandex_api.search(
            text="fix",
            longitude=39.1992540471059,
            latitude=51.66032237776534,
        )

    with allure.step("Проверить, что статус ответ равен 200"):
        assert response.status_code == 200

    with allure.step("Разобрать тело ответа в JSON"):
        data = response.json()

    with allure.step("Проверить заголовок результата поиска"):
        assert data["header"]["text"].startswith("Найдено")

    with allure.step("Проверить заголовок результата поиска"):
        places_blocks = [b for b in data["blocks"] if b["type"] == "places"]
        assert places_blocks
        places = places_blocks[0]["payload"]
        assert len(places) > 0


@pytest.mark.api
@allure.parent_suite("API-тесты")
@allure.suite("Поиск по запросу")
@allure.feature("Поиск по API")
@allure.story("Поиск по числовому тексту")
@allure.title("Поиск по запросу по цифрам")
@allure.description(
    "Отправляем запрос поиска по числовому тексту '45' "
    "с корректными координатами. Ожидаем успешный ответ 200 "
    "и непустой список мест."
)
@allure.severity(allure.severity_level.CRITICAL)
def test_search_number(yandex_api) -> None:
    """
    Поиск по запросу по цифрам
    """
    with allure.step("Отправить запрос поиска по цифрам '45'"):
        response = yandex_api.search(
            text="45",
            longitude=39.199254047105924,
            latitude=51.66032237776534,
        )

    with allure.step("Проверить, что статус ответ равен 200"):
        assert response.status_code == 200

    with allure.step("Разобрать тело ответа в JSON"):
        data = response.json()

    with allure.step("Проверить заголовок результата поиска"):
        assert data["header"]["text"].startswith("Найден")

    with allure.step("Проверить, что блок places не пустой"):
        places_blocks = [b for b in data["blocks"] if b["type"] == "places"]
        assert places_blocks
        places = places_blocks[0]["payload"]
        assert len(places) > 0


@pytest.mark.api
@allure.parent_suite("API-тесты")
@allure.suite("Поиск по запросу")
@allure.feature("Поиск по API")
@allure.story("Поиск с неккоректной широтой")
@allure.title("Поиск с неккоректной широтой(ожидаем 400)")
@allure.description(
    "Отправляем запрос поиска по тексту 'бананы' с неккоректным значением "
    "широты ('фывпап') и корректной долготой. Ожидаем ответ 400 и сообщение "
    "об ошибке с указанием поля location.latitude."
)
@allure.severity(allure.severity_level.CRITICAL)
def test_search_invalid_latitude(yandex_api) -> None:
    """
    Поиск с неккоректной широтой
    """
    with allure.step("Отправить запрос поиска с указанием неккоректной широты"):
        response = yandex_api.search(
            text="бананы",
            longitude=39.2062592316922,
            latitude="фывпап",
        )

    with allure.step("Проверить, что статус ответ равен 400"):
        assert response.status_code == 400

    with allure.step("Разобрать тело ответа в JSON"):
        data = response.json()

    with allure.step("Проверить структуру и сообщение об ошибке"):
        assert data["code"] == "400"
        assert "message" in data
        assert "location.latitude" in data["message"]


@pytest.mark.api
@allure.parent_suite("API-тесты")
@allure.suite("Поиск по запросу")
@allure.feature("Поиск по API")
@allure.story("Поиск с неккоректной долготой")
@allure.title("Поиск с неккоректной долготой(ожидаем 400)")
@allure.description(
    "Отправляем запрос поиска по тексту 'бананы' с неккоректным значением "
    "долготы ('abcd') и корректной широтой. Ожидаем ответ 400 и сообщение "
    "об ошибке с указанием поля location.longitude."
)
@allure.severity(allure.severity_level.CRITICAL)
def test_search_invalid_longitude(yandex_api) -> None:
    """
    Поиск с неккоректной долготой
    """
    with allure.step("Отправить запрос поиска с указанием неккоректной долготой"):
        response = yandex_api.search(
            text="бананы",
            longitude="abcd",
            latitude=200.6796935897011456,
        )

    with allure.step("Проверить, что статус ответ равен 400"):
        assert response.status_code == 400

    with allure.step("Разобрать тело ответа в JSON"):
        data = response.json()

    with allure.step("Проверить структуру и сообщение об ошибке"):
        assert data["code"] == "400"
        assert "message" in data
        assert "location.longitude" in data["message"]
