import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver


class CartPage:
    def __init__(self, driver: WebDriver, ui_url: str) -> None:
        self.__url = ui_url
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)

    @allure.step("Перейти на страницу корзины")
    def go(self) -> None:
        cart_button = self._wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[contains(text(),'Перейти в корзину')"
                    "]/ancestor::a | "
                    "//*[contains(text(),'Перейти в корзину')"
                    "]/ancestor::button"
                )
            )
        )
        cart_button.click()

    @allure.step("Перейти на страницу оформления заказа")
    def product_to_checkout(self) -> None:
        checkout_button = self._wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[contains(text(),'Оформить заказ') or contains(text(),"
                    "'К оформлению')]"
                )
            )
        )
        checkout_button.click()

    @allure.step("Проверяет, что открыт шаг оформления (до оплаты)")
    def is_checkout_step_visible(self) -> bool:
        try:
            self._wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[contains(text(),'Способ оплаты')"
                        " or contains(text(),'Способ доставки')]"
                    )
                )
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Проверить, что товар с названием '{name}' есть в корзине")
    def has_product(self, name: str) -> bool:
        try:
            self._wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//*[contains(text(), '{name}')]"
                    )
                )
            )
            return True
        except TimeoutException:
            return False
