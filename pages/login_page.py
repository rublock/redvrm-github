from selenium.webdriver.common.by import By
import pages.catalog_page as cp
import pages.config_redvrm as config_redvrm


class LoginPage(cp.CatalogPage):
    """Страница входа в систему"""

    # ЛОКАТОРЫ:
    USERNAME_INPUT = (By.XPATH, '//div/input[@name="name"]')
    PASSWORDS_INPUT = (By.XPATH, '//div/input[@name="password"]')
    AUTHENTICATOR_DROPDOWN = (By.XPATH, '//div[@role="combobox"]')
    AUTHENTICATORS = (By.XPATH, "//div/ul/li")
    SUBMIT_BUTTON = (By.XPATH, '//button[@data-cy="login-submit"]')
    CHECKBOX_FOR_LICENSE_AGREEMENT = (By.CSS_SELECTOR, "span.MuiCheckbox-root")
    CONTINUE_BUTTON = (By.XPATH, '//button[contains(text(), "Продолжить")]')
    ERROR_MESSAGE = (By.ID, "errorMessage")
    SECTION_USERS = (By.XPATH, "//h1[text()='Пользователи']")
    SECTION_WORK_SPACES = (By.XPATH, "//h1[text()='Витрина ресурсов']")

    ADMINISTRATOR_USERNAME = config_redvrm.ADMINISTRATOR_USERNAME
    ADMINISTRATOR_PASSWORD = config_redvrm.ADMINISTRATOR_PASSWORD
    DEFAULT_AUTHENTICATOR = config_redvrm.DEFAULT_AUTHENTICATOR

    def __init__(self, driver):
        """
        Инициализирует объект LoginPage
        :param driver: Экземпляр WebDriver.
        """
        super().__init__(driver)

    def login_admin(self, username=None, password=None, authenticator=None):
        """
        Выполняет вход в систему с указанными именем администратора и паролем.

        :param username: Имя пользователя для входа.
        :param password: Пароль для входа.
        :param authenticator: Аутентификатор для входа.
        """
        username = username or self.ADMINISTRATOR_USERNAME
        password = password or self.ADMINISTRATOR_PASSWORD
        authenticator = authenticator or self.DEFAULT_AUTHENTICATOR
        # Ввод данных авторизации
        self._enter_login(username)
        self._enter_password(password)
        # Выбор аутентификатора
        self._choose_authenticator(authenticator)
        # Нажать кнопку "Войти"
        self._click_submit_button()
        # Принять лицензионное соглашение
        self._accept_license_agreement()
        # Проверка, что вход в личный кабинет осуществлен
        assert self.wait_for_element(
            self.SECTION_USERS
        ), "Вход в личный кабинет администратора не осуществлен"

    def login_user(self, username, password, authenticator=None, error_name=None):
        """
        Выполняет вход в систему с указанными именем пользователя и паролем.

        :param username: Имя пользователя для входа.
        :param password: Пароль для входа.
        :param authenticator: Аутентификатор для входа.
        """
        authenticator = authenticator or self.DEFAULT_AUTHENTICATOR
        # Ввод данных авторизации
        self._enter_login(username)
        self._enter_password(password)
        # Выбор аутентификатора
        self._choose_authenticator(authenticator)
        # Нажать кнопку "Войти"
        self._click_submit_button()
        # Проверка, что вход в личный кабинет пользователя осуществлен
        if error_name == 'validation':
            self.check_notification('Не удалось авторизоваться')
        else:
            assert self.wait_for_element(
                self.SECTION_WORK_SPACES
            ), "Вход в личный кабинет пользователя не осуществлен"

    # Приватные методы:

    def _enter_login(self, login):
        """
        Вводит имя пользователя в поле ввода имени пользователя.
        :param login: Имя пользователя для ввода.
        """
        self.input_text(*self.USERNAME_INPUT, text=login)

    def _enter_password(self, password):
        """
        Вводит пароль пользователя в поле ввода пароля.
        :param password: Пароль для ввода.
        """
        self.input_text(*self.PASSWORDS_INPUT, text=password)

    def _choose_authenticator(self, authenticator):
        """
        Выбирает аутентификатор из выпадающего списка.
        :param authenticator: Имя аутентификатора.
        """
        self.click_element(self.AUTHENTICATOR_DROPDOWN)
        self.select_dropdown_by_visible_text(self.AUTHENTICATORS, text=authenticator)

    def _click_submit_button(self):
        """Нажимает кнопку 'Войти'"""
        self.click_element(self.SUBMIT_BUTTON)

    def _click_continue_button(self):
        """Нажимает кнопку 'Продолжить'"""
        self.click_element(self.CONTINUE_BUTTON)

    def _accept_license_agreement(self):
        """Отмечает чекбокс лицензионного соглашения и нажимает 'Продолжить'"""
        self.set_checkbox(self.CHECKBOX_FOR_LICENSE_AGREEMENT)
        self._click_continue_button()
