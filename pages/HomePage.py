import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver


class HomePage:
    def __init__(self, driver: WebDriver, ui_url: str) -> None:
        self.__url = ui_url
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)

    @allure.step("Переходит на главную страницу")
    def go(self) -> None:
        self._driver.get(self.__url)

    @allure.step("Полностью проходит окно «Уточните/Укажите адрес доставки»:"
                 "открывает поле, вводит адрес и подтверждает.")
    def confirm_address(self) -> None:
        try:
            popup = self._wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@role='dialog']")
                )
            )
            button = popup.find_element(By.XPATH, ".//button[1]")
            button.click()

            address_input = self._wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "input[data-testid='address-input']")
                )
            )
            address_input.clear()
            address_input.send_keys("площадь Генерала Черняховского, 1")
            address_input.send_keys("\n")

            button_ok = self._wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[@role='dialog']//button[.//span[normalize-"
                        "space(text())='ОК']]"
                    )
                )
            )
            button_ok.click()

            self._wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "a[data-place-slug]")
                )
            )

        except TimeoutException:
            pass

    @allure.step("Перейти в магазин 'Магнит' из списка магазинов")
    def go_to_magnit_store(self) -> None:
        locators = [
            (By.XPATH, "//*[contains(text(),'Магнит')]/ancestor::a"),
            (
                By.XPATH,
                "//img[@data-testid='smart-image-img' and "
                "contains(@src, "
                "'2224ef8c976f325090b4f4f79777f35a.png')]/ancestor::a"
            ),
        ]
        for by, value in locators:
            for _ in range(3):  # до 3 попыток на случай stale
                try:
                    magnit_button = self._wait.until(
                        EC.element_to_be_clickable((by, value))
                    )
                    self._driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});",
                        magnit_button
                    )
                    self._driver.execute_script("arguments[0].click();",
                                                magnit_button)
                    return
                except (StaleElementReferenceException, TimeoutException):
                    continue

        raise TimeoutException("Магнит не найден в списке магазинов")

    @allure.step(
        "Нажать на товар 'Газированный напиток Evervess Кола 1 л'"
    )
    def select_product(self) -> None:
        ham_button = self._wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                '//a[contains(@class, "UiKitDesktopProductCard_fakeWrapper") '
                'and contains(@aria-label, "Evervess")]',
            ))
        )
        self._driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            ham_button
        )
        self._driver.execute_script("arguments[0].click();", ham_button)

    @allure.step("Нажать на кнопку 'Добавить'")
    def add_product_to_cart(self) -> None:
        add_button = self._wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "button[data-testid='product-full-card-add-to-cart']"
                )
            )
        )
        # 1. Скроллим к элементу
        self._driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            add_button
        )

        # 2. Кликаем по нему из JS
        self._driver.execute_script("arguments[0].click();", add_button)

    @allure.step(
        "Получить название товара из мини-корзины справа "
        "(ожидается 'Газированный напиток Evervess Кола 1 л')"
    )
    def get_cart_item_name_from_mini_cart(self) -> str:
        expected_name = "Газированный напиток Evervess Кола 1 л"

        try:
            mini_cart = self._wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div.s1bnxeqd")
                )
            )
        except TimeoutException:
            raise AssertionError(
                "Мини-корзина не появилась — возможно, "
                "товар не добавился или верстка изменилась"
            )

        try:
            item_el = mini_cart.find_element(
                By.XPATH,
                ".//button[contains(@aria-label, '{name}')]".format(
                    name=expected_name
                ),
            )
            return item_el.get_attribute("aria-label")
        except NoSuchElementException:
            raise AssertionError(
                f"В мини-корзине нет товара '{expected_name}'"
            )

    @allure.step("Нажимает на кнопку 'Оформить заказ'")
    def proceed_to_checkout(self) -> None:
        button_checkout = self._wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[.//span[normalize-space(text())="
                    "'Оформить заказ']]"
                )
            )
        )
        self._driver.execute_script("arguments[0]."
                                    "scrollIntoView({block: 'center'});",
                                    button_checkout)
        self._driver.execute_script("arguments[0].click();",
                                    button_checkout)

