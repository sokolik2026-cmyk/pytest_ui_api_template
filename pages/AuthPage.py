import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class AuthPage:
    def __init__(self, driver: WebDriver, ui_auth_url: str) -> None:
        self.__url = ui_auth_url
        self.__driver = driver
        self.__wait = WebDriverWait(self.__driver, 15)

    @allure.step("Перейти на страницу авторизации")
    def go(self) -> None:
        self.__driver.get(self.__url)

    @allure.step("Ввести логин")
    def add_login(self, user_name: str) -> None:
        login = self.__wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[data-testid='text-field-input']")
            )
        )
        login.clear()
        login.send_keys(user_name)

    @allure.step("Ввести пароль")
    def add_password(self, password: str) -> None:
        password_input = self.__wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[type='password']")
            )
        )
        password_input.clear()
        password_input.send_keys(password)

    @allure.step("Нажимает на кнопку 'Еще'")
    def add_else(self) -> None:
        button = self.__wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "button[data-testid='split-add-user-more-button']"
                )
            )
        )
        button.click()

    @allure.step("Нажимает на кнопку 'Войти'")
    def submit(self) -> None:
        button = self.__wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[.//span[normalize-space(text())=""'Войти']]"
                )
            )
        )
        button.click()

    @allure.step("Нажимает на кнопку 'Войти по логину'")
    def click_login_by(self) -> None:
        button = self.__wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "div[data-testid='menu-option-switchToLogin']"
                )
            )
        )
        button.click()

    @allure.step(
        "Нажимает на кнопку 'Далее' на шаге подтверждения пароля."
    )
    def click_password_next(self) -> None:
        button = self.__wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "button[data-testid='password-next']"
                )
            )
        )
        button.click()

    @allure.step("Проверить, что открыт шаг 'Безопасный вход'")
    def is_on_secure_login_step(self) -> bool:
        dialog = self.__wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(., 'Безопасный вход')]"
                    "[.//button//span[normalize-space(text())="
                    "'Подтвердить']]"
                )
            )
        )
        return dialog.is_displayed()

    @allure.step("Проверяет, что открыт экран логина.")
    def is_login_page_opened(self) -> bool:
        try:
            self.__wait.until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "form[data-testid='page-split-add-user']"
                    )
                )
            )
            return True
        except TimeoutException:
            return False
