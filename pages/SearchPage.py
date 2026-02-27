import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver


class SearchPage:
    def __init__(self, driver: WebDriver, ui_url: str) -> None:
        self.__url = ui_url
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)

    @allure.step("Перейти на страницу поиска")
    def go(self) -> None:
        self._driver.get(self.__url)

    @allure.step("Ищет товар по названию: {value}")
    def search_product(self, value: str):
        search_field = self._wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "input[role='combobox'][placeholder*="
                     "'Найти ресторан']"
                )
            )
        )
        search_field.clear()
        search_field.send_keys(value)
        return self

    @allure.step("Нажимает на кнопку 'Найти'")
    def submit_search(self):
        button_submit = self._wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[text()='Найти']]")
            )
        )
        button_submit.click()
        return self

    @allure.step("Проверяет что товар '{product_name}' в результатах поиска")
    def has_product_in_results(self, product_name: str) -> bool:
        try:
            self._wait.until(
                EC.presence_of_element_located(
                    (By.XPATH,  f"//*[contains(text(), '{product_name}')]")
                )
            )
            return True
        except TimeoutException:
            return False

    @allure.step(
        "Проверяет, что по запросу ничего не найдено"
                 " (экран 'Ничего не нашли,но есть:')"
    )
    def is_not_result_message_visible(self) -> bool:
        try:
            self._wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//h1[contains(text(), 'Ничего не нашли, но есть:')]"
                    )
                )
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Открывает первое заведение из результатов поиска.")
    def open_first_place(self) -> None:
        first_place = self._wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "[data-testid='place-header-root']")
            )
        )
        self._first_place_title = first_place.find_element(
            By.CSS_SELECTOR,
            "[data-testid='place-header-title']"
        ).text
        first_place.click()

    @allure.step(
        "Проверяет, что открыта страница заведения,"
        "и её заголовок совпадает с названием из результатов поиска."
    )
    def is_place_page_opened(self) -> bool:
        try:
            title_elem = self._wait.until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "[data-testid='place-header-title']")
                )
            )
            current_title = title_elem.text
            return current_title == getattr(self, "_first_place_title", None)
        except TimeoutException:
            return False
