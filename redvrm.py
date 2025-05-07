"""ФАЙЛ СО ВСЕМИ СТРАНИЦАМИ РЕД ВРМ"""

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

class BasePage:
    """
    Базовый класс для веб-страниц.
    Обеспечивает общие методы для взаимодействия с элементами
    """

    # АДРЕС БРОКЕРА
    BASE_URL = "http://10.81.112.164/"

    # ЗНАЧЕНИЯ АВТОРИЗАЦИИ ПО УМОЛЧАНИЮ
    ROOT_USERNAME = "root"
    ROOT_PASSWORD = "qqqwww"
    ADMINISTRATOR_USERNAME = "admin"
    ADMINISTRATOR_PASSWORD = "admin"
    USER_USERNAME = "user"
    USER_PASSWORD = "user"
    DEFAULT_AUTHENTICATOR = "DataBase"

    # ЛОКАТОР НОТИФИКАЦИЙ:
    NOTIFICATION = (By.CSS_SELECTOR, "div#notistack-snackbar:last-child")

    def __init__(self, driver):
        """
        Инициализирует объект BasePage под управлением WebDriver.
        :param driver: Если True, запускает браузер в headless-режиме.
        """
        # Настройка времени ожидания
        self.default_wait_time = 30
        # Настройка драйвера
        self.driver = driver
        self.driver.implicitly_wait = self.default_wait_time
        self.driver.get(self.BASE_URL)
        # Настройка действий
        self.actions = ActionChains(self.driver)

    def find_element(self, *locator):
        """
        Находит элемент на странице по указанному локатору.
        :param locator: Локатор элемента (например, XPath, CSS селектор).
        :return: Найденный элемент.
        """
        return self.driver.find_element(*locator)

    def find_elements(self, *locator):
        """
        Находит несколько элементов на странице по указанному локатору.
        :param locator: Локатор элементов (например, XPath, CSS селектор).
        :return: Список найденных элементов.
        """
        return self.driver.find_elements(*locator)

    def wait_for_element(self, locator, condition="presence", timeout=None):
        """
        Ожидает появления элемента на странице.

        :param locator: Локатор элемента (например, XPath, CSS селектор).
        :param condition: Стратегия ожидания, по умолчанию - появления элемента на странице.
        :param timeout: Время ожидания в секундах. Если не указано, используется значение по умолчанию.
        :return: Найденный элемент.
        """
        conditions = {
            "presence": EC.presence_of_element_located,
            "visible": EC.visibility_of_element_located,
            "clickable": EC.element_to_be_clickable,
            "invisible": EC.invisibility_of_element,
        }

        if isinstance(condition, str):
            condition = conditions.get(condition, EC.presence_of_element_located)

        if timeout is None:
            timeout = self.default_wait_time

        wait = WebDriverWait(self.driver, timeout)
        return wait.until(condition(locator))

    def click_element(self, *locator, timeout=None, js_click=False, scroll=False):
        """
        Кликает на элемент на странице.
        :param locator: Локатор элемента (например, XPath, CSS селектор).
        :param timeout: Время ожидания в секундах. Если не указано, используется значение по умолчанию.
        :param js_click: Если True, используется JavaScript для клика.
        :param scroll: Если True, элемент прокручивается в видимую область перед кликом.
        """
        element = self.wait_for_element(*locator, timeout=timeout)
        if js_click:
            self.driver.execute_script("arguments[0].click();", element)
        else:
            if scroll:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView(true);", element
                )
            element.click()

    def click_elements(self, *locator, index=None):
        """
        Кликает на элемент из списка элементов на странице.
        :param locator: Локатор элементов (например, XPath, CSS селектор).
        :param index: Индекс элемента, на который нужно кликнуть. Если не указан, кликает на первый элемент.
        """
        elements = self.find_elements(*locator)
        if index is not None:
            elements[index].click()
        else:
            elements[0].click()

    def input_text(
        self, *locator, text, clear=True, send_keys=True, click=False, timeout=None
    ):
        """
        Вводит текст в элемент на странице.

        :param locator: Локатор элемента (например, XPath, CSS селектор).
        :param text: Текст для ввода.
        :param clear: Если True, очищает текстовое поле перед вводом.
        :param send_keys: Если True, отправляет текст в поле.
        :param click: Если True, кликает на элемент перед вводом текста.
        :param timeout: Время ожидания в секундах. Если не указано, используется значение по умолчанию.
        """
        element = self.wait_for_element(locator, condition="visible", timeout=timeout)
        if click:
            self.click_element(locator)
        if clear:
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.DELETE)
            self.actions.key_down(Keys.SHIFT).key_down(Keys.ALT).click(element).key_up(
                Keys.ALT
            ).key_up(Keys.SHIFT).perform()
        if send_keys:
            element.send_keys(text)

    def select_dropdown_by_visible_text(self, locator, text, timeout=None):
        """
        Выбирает элемент из выпадающего списка по тексту.
        :param locator: Локатор элемента <li>.
        :param text: Текст, который нужно выбрать.
        :param timeout: Время ожидания в секундах. Если не указано, используется значение по умолчанию.
        """
        # Ждем, пока элементы не будут видны
        elements = self.wait_for_element(locator, condition="visible", timeout=timeout)
        # Находим все элементы списка по локатору
        elements = self.find_elements(*locator)
        # Перебираем элементы и кликаем по нужному тексту
        for element in elements:
            if element.text == text:
                element.click()
                break
        else:
            raise ValueError(f"Не найден элемент с текстом: {text}")

    # def get_text(self, by, locator):
    #     """
    #     :param by:
    #     :param locator: Локатор элемента <select>.
    #     """
    #     element = self.driver.find_element(by, locator)
    #     return element.text

    def get_text(self, locator):
        """
        Извлекает текст с элемента на странице.
        :param locator: Локатор элемента.
        """
        element = self.driver.find_element(locator)
        return element.text

    def check_notification(self, expected_message):
        """
        Проверяет всплывающее окно с оповещением о действии.
        :param expected_message: Ожидаемое оповещение.
        """
        element = self.wait_for_element(self.NOTIFICATION, condition="visible")
        assert element.text == expected_message
        self.wait_for_element(self.NOTIFICATION, condition="invisible")

    def press_enter(self):
        """
        Отправляет клавишу Enter.
        """
        self.actions.send_keys(Keys.ENTER).perform()

    def assert_current_url(self, expected_url, timeout=None):
        """
        Проверяет, что текущий URL соответствует ожидаемому, с ожиданием.
        :param expected_url: Ожидаемый URL.
        :param timeout: Максимальное время ожидания (в секундах).
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_to_be(expected_url))
        except Exception as e:
            raise AssertionError(
                f"Ожидался URL: {expected_url}, но был: {self.driver.current_url}. "
                f"Превышено время ожидания {timeout} секунд."
            )

    # TODO Методы для смены темы и справки "О программе"


class CataloguePage(BasePage):
    """
    Базовый класс для страниц, содержащих каталоги.
    Обеспечивает методы для работы с каталогами.
    """

    # ЛОКАТОРЫ ПУНКТОВ МЕНЮ
    THEME_SWITCH_BUTTON = (By.XPATH, '//div[@data-testid="theme-switch"]')
    ADMIN_PAGE_BUTTON = (By.CSS_SELECTOR, 'button:nth-child(5)')
    ABOUT_BUTTON = (By.XPATH, '//div[@data-testid="sidebar-about"]')

    # ЛОКАТОРЫ ПУНКТОВ МЕНЮ КАТАЛОГА:
    CREATE_BUTTON = (By.XPATH, '//button[@data-testid="create-button"]')
    EDIT_BUTTON = (By.XPATH, '//button[@data-testid="edit-button"]')
    DELETE_BUTTON = (By.XPATH, '//button[@data-testid="delete-button"]')

    # ЛОКАТОРЫ ВЫБОРА СТОЛБЦОВ:
    COLUMNS = (By.XPATH, '//button[text()="Столбцы"]')
    SEARCH = (By.XPATH, '//input[@type="text"]')
    COLUMNS_LIST = (By.XPATH, "//div/label")
    RESET = (By.XPATH, '//button[text()="Reset"]')

    # ОБЩИЕ ЛОКАТОРЫ КАТАЛОГА:
    # COLUMNS_HEADERS = (By.XPATH, '//div[@role="columnheader"]')
    ROWS = (By.XPATH, '//div[@role="rowgroup"]')
    DROPDOWN_LIST = (By.XPATH, '//ul[@role="listbox"]/li')
    FORM_SUBMIT = (By.XPATH, '//button[@data-testid="form-drawer-submit"]')

    # ЛОКАТОРЫ ПОДТВЕРЖДЕНИЯ УДАЛЕНИЯ
    CANCEL_DELETE = (By.XPATH, '//div[@role="dialog"]/div[2]/div[1]')
    CONFIRM_DELETE = (By.XPATH, '//div[@role="dialog"]/div[2]/div[2]')

    # ЛОКАТОРЫ СТРОКИ СОСТОЯНИЯ
    SELECT_ALL = (By.XPATH, '//input[@aria-label="Выбрать все строки"]')
    STRINGS_ON_PAGE = (By.XPATH, '//div[@aria-haspopup="listbox"]')
    PREVIOUS_BUTTON = (
        By.XPATH, '//div[@class="MuiTablePagination-actions"]/button[1]')
    NEXT_BUTTON = (
        By.XPATH, '//div[@class="MuiTablePagination-actions"]/button[2]')

    def __init__(self, driver):
        """
        Инициализирует объект CataloguePage.
        :param driver: Экземпляр WebDriver.
        """
        self.BASE_URL = self.BASE_URL + 'admin'
        super().__init__(driver)

    def show_column(self, column):
        """
        Показывает в списке только одну колонку.
        :param column: Колонка для отображения.
        """
        # Открыть меню выьора столбцов
        self._click_columns_button()
        # Очистить выбор всех столбцов
        self._clear_columns()
        # Выбор столбца
        self._select_column(column)
        # TODO: Проверка отображения

    def show_columns(self, columns):
        """
        Показывает в списке переданные колонки.
        :param columns: Список колонок для отображения.
        """
        # Открыть меню выбора столбцов
        self._click_columns_button()
        # Очисить выбор всех столбцов
        self._clear_columns()
        # Выбор столбцов
        for column in columns:
            self._select_column(column)
        # Завершение выбора столбцов
        self._click_columns_button()
        # TODO: Проверка отображения

    def select_row(self, row):
        """
        Выбирает одну строку из списка страницы-каталога.
        :param row: Строка для выбора.
        """
        self._select_row(row)

    def select_rows(self, rows):
        """
        Выбирает переданные строки из списка страницы-каталога.
        :param rows: Список строк для выбора.
        """
        for row in rows:
            self._select_row(row)

    def open_page(self, page):
        """
        Открывает страницу из левого меню системы.
        :param page: Открываемая страница.
        """
        # Генерация словаря страниц
        names = ("Аутентификаторы", "Группы", "Пользователи",
                 "Агенты", "Поставщики", "Пулы",
                 "Рабочие места",
                 "Лицензии", "Сессии",
                 "Разрешения", "Группы доступа",
                 "Страница пользователя")
        values = range(len(names))
        pages = dict(zip(names, values))

        # Выбор нужного раздела
        if pages[page] in range(3):
            self._unfold_section("Учётные записи")
        elif pages[page] in range(3, 6):
            self._unfold_section("Ресурсы")
        elif pages[page] in range(7, 9):
            self._unfold_section("Лицензирование")
        elif pages[page] in range(9, 11):
            self._unfold_section("Настройки")

        # Переход на страницу
        page_selector = (By.XPATH, f'//span[text()="{page}"]/../../..')
        self.wait_for_element(page_selector, condition="visible")
        self.click_element(page_selector)

    # Приватные методы

    def _unfold_section(self, section):
        """
        Разворачивает раздел в левом меню системы.
        :param section: Разворачиваемый раздел.
        """
        section_selector = (By.XPATH, f'//span[text()="{section}"]/../../..')
        self.click_element(section_selector)

    def _click_create_button(self):
        """Открывает модальное окно создания пользователя"""
        self.wait_for_element(self.CREATE_BUTTON, condition="clickable")
        self.click_element(self.CREATE_BUTTON)
        self.wait_for_element(self.FORM_SUBMIT)

    def _click_edit_button(self):
        """Открывает модальное окно изменения пользователя"""
        self.wait_for_element(self.EDIT_BUTTON, condition="clickable")
        self.click_element(self.EDIT_BUTTON)
        self.wait_for_element(self.FORM_SUBMIT)

    def _click_delete_button(self):
        """Инициирует удаление пользователя"""
        self.wait_for_element(self.DELETE_BUTTON, condition="clickable")
        self.click_element(self.DELETE_BUTTON)
        self.wait_for_element(self.CONFIRM_DELETE)

    def _click_columns_button(self):
        """Открывает меню выбора столбцов для показа"""
        self.wait_for_element(self.COLUMNS, condition="clickable")
        self.click_element(self.COLUMNS)

    def _select_column(self, column):
        """
        Выделяет переданную колонку.
        :param column: Колонка для выбора.
        """
        self.select_dropdown_by_visible_text(self.COLUMNS_LIST, column)

    def _clear_columns(self):
        """Снимает галочки со всех пунктов в меню выбора колонок"""
        self._select_column("Show/Hide All")

    def _select_row(self, row):
        """
        Выбирает переданную запись.
        :param row: Запись для удаления.
        """
        row_selector = (By.XPATH, f'//div[text()="{row}"]/../div[2]')
        self.wait_for_element(self.ROWS, condition="visible")
        self.click_element(row_selector)

    def _click_form_submit(self):
        """Закрывает модальное окно, завершая действие"""
        self.wait_for_element(self.FORM_SUBMIT, condition="clickable")
        self.click_element(self.FORM_SUBMIT)

    def _click_confirm_delete(self):
        """Подтверждает удаление записи из каталога"""
        self.wait_for_element(self.CONFIRM_DELETE, condition="clickable")
        self.click_element(self.CONFIRM_DELETE)

    def _click_cancel_delete(self):
        """Отменяет удаление записи в каталоге"""
        self.wait_for_element(self.CANCEL_DELETE, condition="clickable")
        self.click_element(self.CANCEL_DELETE)

    def _click_admin_page(self):
        """Переходит на страницу администратора из меню пользователя"""
        self.click_element(self.ADMIN_PAGE_BUTTON)

    def _click_change_theme(self):
        """Меняет тему оформления системы"""
        self.click_element(self.THEME_SWITCH_BUTTON)

    def _click_about(self):
        """Вызывает окно справки о программе"""
        self.click_element(self.ABOUT_BUTTON)


class LoginPage(CataloguePage):
    """Страница входа в систему"""

    USERNAME_INPUT = (By.XPATH, '//div/input[@name="name"]')
    PASSWORDS_INPUT = (By.XPATH, '//div/input[@name="password"]')
    AUTHENTICATOR_DROPDOWN = (By.XPATH, '//div[@role="combobox"]')
    AUTHENTICATORS = (By.XPATH, "//div/ul/li")
    SUBMIT_BUTTON = (By.XPATH, '//button[@data-cy="login-submit"]')
    CHECKBOX_FOR_LICENSE_AGREEMENT = (
        By.XPATH, '//span/input[@type="checkbox"]')
    CONTINUE_BUTTON = (By.XPATH, '//button[contains(text(), "Продолжить")]')
    ERROR_MESSAGE = (By.ID, "errorMessage")

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

    def login_user(self, username=None, password=None, authenticator=None):
        """
        Выполняет вход в систему с указанными именем пользователя и паролем.

        :param username: Имя пользователя для входа.
        :param password: Пароль для входа.
        :param authenticator: Аутентификатор для входа.
        """
        username = username or self.USER_USERNAME
        password = password or self.USER_PASSWORD
        authenticator = authenticator or self.DEFAULT_AUTHENTICATOR
        # Ввод данных авторизации
        self._enter_login(username)
        self._enter_password(password)
        # Выбор аутентификатора
        self._choose_authenticator(authenticator)
        # Нажать кнопку "Войти"
        self._click_submit_button()

    # Приватные методы
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
        self.wait_for_element(self.AUTHENTICATORS, condition="visible")
        self.select_dropdown_by_visible_text(
            self.AUTHENTICATORS, text=authenticator)

    def _click_submit_button(self):
        """Нажимает кнопку 'Войти'"""
        self.click_element(self.SUBMIT_BUTTON)

    def _click_continue_button(self):
        """Нажимает кнопку 'Продолжить'"""
        self.click_element(self.CONTINUE_BUTTON)

    def _accept_license_agreement(self):
        """Отмечает чекбокс лицензионного соглашения и нажимает 'Продолжить'"""
        self.click_element(self.CHECKBOX_FOR_LICENSE_AGREEMENT)
        self._click_continue_button()


class AuthenticatorsPage(CataloguePage):
    """Страница "Аутентификаторы" раздела "Учётные записи"."""

    # ЛОКАТОРЫ ПУНКТОВ МЕНЮ:
    CHECK_CONNECTION = (By.XPATH, '//button[text()="Проверить соединение"]')

    # ЛОКАТОРЫ ФОРМЫ СОЗДАНИЯ АУТЕНТИФИКАТОРА:
    NAME = (By.XPATH, '//input[@name="auth_name"]')
    DESCRIPTION = (By.XPATH, '//input[@name="comments"]')
    AUTH_TYPE_FIELD = (By.XPATH, '//div[@id="mui-component-select-auth_type"]')

    # ЛОКАТОРЫ НАСТРОЕК АУТЕНТИФИКАТОРОВ:
    HOST_IP = (By.XPATH, '//input[@name="settings.ldap_host"]')
    PORT = (By.XPATH, '//input[@name="settings.ldap_port"]')
    LOGIN = (By.XPATH, '//input[@name="settings.ldap_username"]')
    PASSWORD = (By.XPATH, '//input[@name="settings.ldap_password"]')
    HIDE_PASSWORD = (By.XPATH, '//button[@aria-label="toggle password visibility"]')
    ADVANCED_SETTINGS = (By.XPATH, '//button[text()="Расширенные настройки"]')

    # ЛОКАТОРЫ ДОПОЛНИТЕЛЬНЫХ НАСТРОЕК:
    AUTHORITY = (By.XPATH, '//input[@name="settings.ldap_base"]')
    TIMEOUT = (By.XPATH, '//input[@name="settings.connection_timeout"]')
    SSL_CHECKBOX = (By.XPATH, '//span[text()="использовать SSL"]/../span/input')
    USER_CLASS = (By.XPATH, '//input[@name="settings.ldap_user_class"]')
    ID_ATTRIBUTE = (By.XPATH, '//input[@name="settings.ldap_user_id_attr"]')
    USER_ATTRIBUTE = (By.XPATH, '//input[@name="settings.ldap_username_attr"]')
    GROUP_ATTRIBUTE = (By.XPATH, '//input[@name="settings.ldap_groupname_attr"]')
    ALTERNATIVE_CLASS = (By.XPATH, '//input[@name="settings.alternative_class"]')

    def __init__(self, driver):
        """
        Инициализирует объект AuthenticatorsPage.
        :param driver: Экземпляр WebDriver.
        """
        super().__init__(driver)

    def create_authenticator(self, name, description, auth_type, auth_settings=None):
        """
        Создаёт новый аутентификатор с переданными параметрами

        :param name: Имя аутентификатора.
        :param description: Описание.
        :param auth_type: Тип аутентификатора.
        :param auth_settings: Словарь, содержащий дополнительные настройки для аутентификаторов типа ActiveDirectory и РедАДМ.
        """
        # Нажать кнопку "Создать"
        self._click_create_button()
        # Заполнение полей аутентификатора
        self._enter_name(name)
        self._enter_description(description)
        self._select_type(auth_type)
        # Дополнительные настройки
        self._fill_auth_settings(auth_type, auth_settings)
        # Подтверждение создания аутентификатора
        self._click_form_submit()
        # Проверка нотификации
        self.check_notification("аутентификатор успешно создан")

    def modify_authenticator(
        self,
        authenticator,
        name=None,
        description=None,
        auth_type=None,
        auth_settings=None,
    ):
        """
        Изменяет параметры существующего аутентификатора.

        :param authenticator: Имя существующего аутентификатора для изменения.
        :param name: Новое имя аутентификатора.
        :param description: Новое описание.
        :param auth_type: Новый тип для аутентификатора.
        :param auth_settings: Словарь, содержащий новые дополнительные настройки для аутентификаторов типа ActiveDirectory и РедАДМ, по умолчанию - не изменяется.
        """
        # Выбор аутентификатора для изменения
        self.select_row(authenticator)
        # Нажать кнопку "Изменить"
        self._click_edit_button()
        # Изменение параметров аутентификатора
        if name:
            self._enter_name(name, clear=True)
        if description:
            self._enter_description(description, clear=True)
        if auth_type:
            self._select_type(auth_type)
        if auth_settings:
            self._fill_auth_settings(auth_type, auth_settings, clear=True)
        # Подтверждение изменения
        self._click_form_submit()
        # Проверка нотификации
        self.check_notification("аутентификатор успешно изменён")

    def delete_authenticator(self, authenticator, cancel=False):
        """
        Удаляет аутентификатор по переданному имени.

        :param name: Имя для аутентификатора к удалению.
        :param cancel: Флаг отмены удаления, по умолчанию - не отменять.
        """
        # Выбрать аутентификатор для удаления
        self.select_row(row=authenticator)
        # Нажать кнопку "Удалить"
        self._click_delete_button()
        if cancel:
            # Отмена удаления
            self._click_cancel_delete()
        else:
            # Подтверждение удаления
            self._click_confirm_delete()
            # Проверка нотификации
            self.check_notification("аутентификатор успешно удалён")

    def check_connection(self, authenticator, connection="success"):
        """
        Проверяет соединение выбранного аутентификатора.

        :param authenticator: Аутентификатор для проверки.
        :param connection: Результат проверки подключения, по умолчанию - успешно.
        """
        # Результаты проверок
        connections = {
            "success": "аутентификатор успешно проверен",
            "failed": "Соединение неудачно",
        }

        if isinstance(connection, str):
            connection = connections.get(connection)

        # Выбор аутентификатора для проверки
        self.select_row(row=authenticator)
        # Нажать кнопку проверить соединение
        self._click_check_connection_button()
        # Проверить нотификацию
        self.check_notification(expected_message=connection)

    # Приватные методы

    def _enter_name(self, name, clear=False):
        """
        Вводит имя аутентификатора в поле ввода.

        :param name: Имя аутентификатора.
        :param clear: Флаг для очистки полей ввода, по умолчанию - не очищать.
        """
        self.input_text(*self.NAME, text=name, clear=clear, click=True)

    def _enter_description(self, description, clear=False):
        """
        Вводит описание в поле ввода.

        :param description: Описание аутентификатора.
        :param clear: Флаг для очистки полей ввода, по умолчанию - не очищать.
        """
        self.input_text(*self.DESCRIPTION, text=description, clear=clear, click=True)

    def _select_type(self, auth_type):
        """
        Выбирает тип аутентификатора из выпадающего списка.
        :param auth_type: Тип аутентификатора для выбора.
        """
        self.click_element(self.AUTH_TYPE_FIELD)
        self.select_dropdown_by_visible_text(self.DROPDOWN_LIST, text=auth_type)

    def _enter_host_ip(self, host_ip):
        """
        Вводит адрес хоста аутентификтора в поле ввода.
        :param host_ip: IP-адрес хоста аутентификатора.
        """
        self.input_text(*self.HOST_IP, text=host_ip, clear=True, click=True)

    def _enter_port(self, port):
        """
        Вводит порт подключения к хосту аутентификатора в поле ввода.
        :param port: Порт.
        """
        self.input_text(*self.PORT, text=port, clear=True, click=True)

    def _enter_login(self, login, clear=False):
        """
        Вводит логин авторизации аутентификатора в поле ввода.

        :param login: Логин.
        :param clear: Флаг для очистки полей ввода, по умолчанию - не очищать.
        """
        self.input_text(*self.LOGIN, text=login, clear=clear, click=True)

    def _enter_password(self, password):
        """
        Вводит пароль авторизации аутентификатора в поле ввода.
        :param password: Пароль.
        """
        self.input_text(*self.PASSWORD, text=password, click=True)

    def _toggle_password_visibility(self):
        """Изменяет отображение пароля"""
        self.click_element(self.HIDE_PASSWORD)

    def _click_advanced_settings_button(self):
        """Разворачивает дополнительные настройки"""
        self.wait_for_element(self.ADVANCED_SETTINGS, condition="visible")
        self.click_element(self.ADVANCED_SETTINGS)

    def _enter_authority(self, authority, clear=False):
        """
        Вводит значение зоны видимости аутентификатора в поле ввода.

        :param authority: Зона видимости аутентификатора.
        :param clear: Флаг для очистки полей ввода, по умолчанию - не очищать.
        """
        self.click_element(self.AUTHORITY, scroll=True)
        self.input_text(*self.AUTHORITY, text=authority, clear=clear, click=False)

    def _enter_timeout(self, timeout):
        """
        Вводит значение времени ожидания в поле ввода.
        :param timeout: Таймаут ожидания ответа.
        """
        self.click_element(self.TIMEOUT, scroll=True)
        self.input_text(*self.TIMEOUT, text=timeout, clear=True, click=False)

    def _click_ssl_checkbox(self):
        """Ставит галку в чекбоксе SSL"""
        self.click_element(self.SSL_CHECKBOX, scroll=True)

    def _enter_user_class(self, user_class):
        """
        Вводит пользовательский класс в поле ввода.
        :param user_class: Пользовательский класс.
        """
        self.click_element(self.USER_CLASS, scroll=True)
        self.input_text(*self.USER_CLASS, text=user_class, clear=True, click=False)

    def _enter_id_attribute(self, id_attribute):
        """
        Вводит атрибут ID в поле ввода.
        :param id_attribute: ID-атрибут.
        """
        self.click_element(self.ID_ATTRIBUTE, scroll=True)
        self.input_text(*self.ID_ATTRIBUTE, text=id_attribute, clear=True, click=False)

    def _enter_user_attribute(self, user_attribute):
        """
        Вводит атрибут пользователя аутентификатора в поле ввода.
        :param user_attribute: Атрибут пользователя.
        """
        self.click_element(self.USER_ATTRIBUTE, scroll=True)
        self.input_text(*self.USER_ATTRIBUTE, text=user_attribute, clear=True)

    def _enter_group_attribute(self, group_attribute):
        """
        Вводит атрибут группы аутентификатора в поле ввода.
        :param group_attribute: Атрибут группы.
        """
        self.click_element(self.GROUP_ATTRIBUTE, scroll=True)
        self.input_text(
            *self.GROUP_ATTRIBUTE, text=group_attribute, clear=True, click=False
        )

    def _enter_alternative_class(self, alternative_class, clear=False):
        """
        Вводит альтернативный класс аутентификатора в поле ввода.

        :param alternative_class: Альтернативный класс.
        :param clear: Флаг для очистки полей ввода, по умолчанию - не очищать.
        """
        self.click_element(self.ALTERNATIVE_CLASS, scroll=True)
        self.input_text(
            *self.ALTERNATIVE_CLASS, text=alternative_class, clear=clear, click=False
        )

    def _fill_advanced_settings(self, advanced_settings, clear=False):
        """
        Заполняет поля дополниьельных настроек аутентификатора.

        :param advanced_settings: Словарь дополнительных настроек аутентификатора.
        :param clear: Флаг для очистки полей ввода, по умолчанию - не очищать.
        """
        self._click_advanced_settings_button()

        # Получение значений дополнительных настроек
        authority = advanced_settings.get("authority", None)
        timeout = advanced_settings.get("timeout", None)
        use_ssl = advanced_settings.get("use_ssl", None)
        user_class = advanced_settings.get("user_class", None)
        id_attribute = advanced_settings.get("id_attibute", None)
        user_attribute = advanced_settings.get("user_attribute", None)
        group_attribute = advanced_settings.get("group_attribute", None)
        alternative_class = advanced_settings.get("alternative_class", None)

        # Заполнение полей
        if authority:
            self._enter_authority(authority, clear)
        if timeout:
            self._enter_timeout(timeout)
        if use_ssl:
            self._click_ssl_checkbox()
        if user_class:
            self._enter_user_class(user_class)
        if id_attribute:
            self._enter_id_attribute(id_attribute)
        if user_attribute:
            self._enter_user_attribute(user_attribute)
        if group_attribute:
            self._enter_group_attribute(group_attribute)
        if alternative_class:
            self._enter_alternative_class(alternative_class, clear)

    def _fill_auth_settings(self, auth_type, auth_settings, clear=False):
        """
        Заполняет поля настроек аутентификатора.

        :param auth_type: Тип аутентификатора для корректировки настроек.
        :param auth_settings: Словарь параметров аутентификатора.
        :param clear: Флаг для очистки полей ввода, по умолчанию - не очищать.
        """
        if auth_type in ("РЕД АДМ", "Active Directory") and auth_settings:
            # Заполнение дополнительных настроек
            advanced_settings = auth_settings.get(
                "advanced_settings", {"use_ssl": True}
            )
            if advanced_settings:
                self._fill_advanced_settings(advanced_settings, clear)

            # Получение значений основных полей
            host_ip = auth_settings.get("host_ip", None)
            port = auth_settings.get("port", None)
            login = auth_settings.get("login", None)
            password = auth_settings.get("password", None)
            # Заполнение основных полей
            if host_ip:
                self._enter_host_ip(host_ip)
            if port:
                self._enter_port(port)
            if login:
                self._enter_login(login, clear)
            if password:
                self._enter_password(password)

    def _click_check_connection_button(self):
        """Инициирует проверку соединения"""
        self.click_element(self.CHECK_CONNECTION)


class GroupsPage(CataloguePage):
    """Страница 'Группы' раздела 'Учетные записи'"""

    # ЛОКАТОРЫ
    ACCOUNTS_PAGE = (By.XPATH, "//span[contains(@class, 'MuiTypography-root') and text() = 'Учётные записи']")
    GROUP_PAGE = (By.XPATH, "//span[contains(@class, 'MuiTypography-root') and text() = 'Группы']")

    GROUP_CREATE_BUTTON = (By.XPATH, "//button[@data-testid='create-button']")
    GROUP_EDIT_BUTTON = (By.XPATH, "//button[@data-testid='edit-button']")
    GROUP_DETAIL_BUTTON = (By.XPATH, "//button[@data-testid='detail-button']")
    GROUP_DELETE_BUTTON = (By.XPATH, "//button[@data-testid='delete-button']")
    CHOOSE_ALL_CHECKBOX = (By.XPATH, "//input[@type='checkbox' and @aria-label='Выбрать все строки']")
    CHOOSE_GROUP_CHECKBOX_BY_NAME = (By.XPATH, "//div[@title='{group_name}']")

    # форма создания
    GROUP_NAME_INPUT = (By.XPATH, "//input[@name='group_name']")
    FORM_CLOSE_BUTTON = (By.XPATH, "//button[@data-testid='CloseIcon']")
    FORM_SUBMIT_BUTTON = (By.XPATH, "//button[@data-testid='form-drawer-submit']")

    #форма редактирования
    GROUP_EDIT_SUBMIT_BUTTON = (By.XPATH, "//button[@data-testid='form-drawer-submit']")
    GROUP_EDIT_CLOSE_BUTTON = (By.XPATH, "//button[@type='button' and @aria-label='Закрыть']")
    GROUP_EDIT_NAME_INPUT = (By.XPATH, "//input[@name='group_name']")

    # страница "Подробнее" (отображает детальную информацию о группе)
    USER_DETAIL_BUTTON = (By.XPATH, "//button[@data-testid='detail-button']")
    USER_CREATE_BUTTON = (By.XPATH, "//button[contains(text(), 'Добавить')]")
    USER_DELETE_BUTTON = (By.XPATH, "//button[contains(text(), 'Удалить')]")
    CHOOSE_USER_CHECKBOX_BY_NAME = (By.XPATH, "//div[@title='{group_name_value}']")

    # модальное окно для добавления пользователей в группу
    NEW_USER_FORM_CLOSE_BUTTON = (By.XPATH, "//button[@type='button' and @aria-label='Закрыть']")
    NEW_USER_OPEN_DROPDOWN_MENU = (By.XPATH, "//label/div[contains(@class, 'css-1xjtrwu') and text() = 'пользователи']")
    NEW_USER_ADD_BUTTON = (By.XPATH, "//button[@data-testid='form-drawer-submit']")

    def __init__(self, driver):
        """
        Инициализирует объект GroupsPage.
        :param driver: Экземпляр WebDriver.
        """
        super().__init__(driver)

    #создание группы
    def create_group(self, group_name=None):
        self._navigate_to_group_page()
        self._click_create_group()
        self._fill_creating_group_form(group_name=group_name)
        self._click_submit_form_group()

    # редактирование группы
    def edit_group(self, group_name=None, edited_group_name=None):
        self._navigate_to_group_page()
        self._choose_existing_group(group_name=group_name)
        self._click_edit_group_button()
        self._fill_edit_group_form(edited_group_name=edited_group_name)
        self._click_edit_group_form_submit()


    def _navigate_to_group_page(self):
        self.click_element(self.ACCOUNTS_PAGE)
        self.click_element(self.GROUP_PAGE)

    def _click_create_group(self):
        """Кликает кнопку создания группы"""
        self.click_element(self.GROUP_CREATE_BUTTON)

    def _fill_creating_group_form(self, group_name=None):
        """
        Заполняет форму для созднания группы.
        :param group_name: имя группы.
        """
        self.input_text(*self.GROUP_NAME_INPUT, text=group_name)

    def _click_submit_form_group(self):
        """Кликает кнопку добавления группы в форме"""
        self.click_element(self.FORM_SUBMIT_BUTTON)

    def _click_edit_group_button(self):
        self.click_element(self.GROUP_EDIT_BUTTON)

    def _choose_existing_group(self, group_name):
        """Ищет строку с именем нужной группы и выбирает её чекбокс"""
        by, xpath_template = self.CHOOSE_GROUP_CHECKBOX_BY_NAME
        formatted_xpath = xpath_template.format(group_name=group_name)
        self.find_element(by, formatted_xpath).click()

    def _fill_edit_group_form(self, edited_group_name=None):
        self.input_text(*self.GROUP_EDIT_NAME_INPUT, text=edited_group_name)

    def _click_edit_group_form_submit(self):
        self.click_element(self.GROUP_EDIT_SUBMIT_BUTTON)


class UsersPage(CataloguePage):
    """Страница "Пользователи" раздела "Учётные записи"."""

    # ЛОКАТОРЫ ПУНКТОВ МЕНЮ
    BLOCK_BUTTON = (By.XPATH, '//button[text()="Заблокировать"]')

    # ЛОКАТОРЫ ФОРМЫ СОЗДАНИЯ ПОЛЬЗОВАТЕЛЯ:
    AUTHENTICATORS_FIELD = (By.XPATH, '//input[@name="auth_strategy"]/../div')
    LOGIN_FIELD = (By.XPATH, '//input[@name="name"]')
    PASSWORD_FIELD = (By.XPATH, '//input[@name="password"]')
    PASSWORD_VISIBILITY = (
        By.XPATH,
        '//button[@aria-label="toggle password visibility"]',
    )
    USER_ROLE = (By.XPATH, '//label[@data-cy="radio-Пользователь"]')
    ADMIN_ROLE = (By.XPATH, '//label[@data-cy="radio-Администратор"]')
    GROUP_FIELD = (By.XPATH, '//input[@name="groups"]')

    def __init__(self, driver):
        """
        Инициализирует объект UsersPage.
        :param driver: Экземпляр WebDriver.
        """
        super().__init__(driver)

    def create_user(
        self,
        authenticator,
        login,
        password,
        show_password=False,
        role="Пользователь",
        group=None,
    ):
        """
        Создаёт нового пользователя с переданными параметрами.

        :param authenticator: Аутентификатор.
        :param login: Логин пользователя.
        :param password: Пароль пользователя.
        :param role: Роль, по-умолчанию - "Пользователь".
        :param group: Группа для выбора, по умолчанию - не задана.
        """
        # Открыть окно создания пользователя
        self._click_create_button()
        # Выбор аутентификатора
        self._select_authenticator(authenticator)
        # Ввод данных пользователя
        self._enter_login(login, clear=False)
        if show_password:
            self._toggle_password_visibility()
        self._enter_password(password)
        # Выбор роли
        self._select_role(role)
        # Выбор группы
        if group:
            self._select_group(group)
        # Завершить создание пользователя
        self._click_form_submit()
        # Проверить нотификации
        self.check_notification("пользователь успешно создан")

    def modify_user(
        self,
        user,
        authenticator=None,
        login=None,
        password=None,
        show_password=False,
        role=None,
        group=None,
    ):
        """
        Изменяет параметры существующего пользователя.

        :param user: Имя существующего пользователя для изменения.
        :param authenticator: Новый аутентификатор, по умолчанию - не изменяется.
        :param login: Новый логин пользователя, по умолчанию - не изменяется.
        :param password: Новый пароль пользователя, по умолчанию - не изменяется.
        :param role: Новая роль для пользователя, по умолчанию - не изменяется.
        :param group: Новая группа для пользователя, по умолчанию - не изменяется.
        """
        # Выбор пользователя для изменения
        self.select_row(user)
        # Открыть окно изменения пользователя
        self._click_edit_button()
        # Изменение параметров
        if authenticator:
            self._select_authenticator(authenticator)
        if login:
            self._enter_login(login, clear=True)
        if password:
            if show_password:
                self._toggle_password_visibility()
            self._enter_password(password)
        if role:
            self._select_role(role)
        if group:
            self._select_group(group)
        # Завершить редактирование пользователя
        self._click_form_submit()
        # Проверка нотификации
        self.check_notification("пользователь успешно изменён")

    def delete_user(self, user, cancel=False):
        """
        Удаляет пользователя.
        :param user: Имя пользователя для удаления.
        :param cancel: Флаг отмены удаления, по умолчанию - не отменять.
        """
        # Выбор пользователя для удаления
        self.select_row(user)
        # Удалить пользователя
        self._click_delete_button()
        if cancel:
            # Отмена удаления
            self._click_cancel_delete()
        else:
            # Подтверждение удаления
            self._click_confirm_delete()
            # Проверка нотификации
            self.check_notification("пользователь успешно удалён")

    # Приватные методы

    def _select_authenticator(self, authenticator):
        """
        Выбирает аутентификатор из выпадающего списка
        :param authenticator: Название аутентификатора для выбора.
        """
        self.click_element(self.AUTHENTICATORS_FIELD)
        self.select_dropdown_by_visible_text(self.DROPDOWN_LIST, text=authenticator)

    def _enter_login(self, login, clear=False):
        """
        Вводит имя пользователя в поле ввода имени пользователя.

        :param login: Имя пользователя для ввода.
        :param clear: Флаг для очистки полей ввода, по умолчанию - не очищать.
        """
        self.input_text(*self.LOGIN_FIELD, text=login, clear=clear, click=True)

    def _toggle_password_visibility(self):
        """Изменяет отображение пароля"""
        self.click_element(self.PASSWORD_VISIBILITY)

    def _enter_password(self, password):
        """
        Вводит пароль пользователя в поле ввода пароля.
        :param password: Пароль для ввода.
        """
        self.input_text(*self.PASSWORD_FIELD, text=password, click=True)

    def _select_role(self, role):
        """
        Выбирает роль из списка радиокнопок.
        :param role: Роль для выбора.
        """
        roles = {"Пользователь": self.USER_ROLE, "Администратор": self.ADMIN_ROLE}

        self.click_element(roles[role])

    def _select_group(self, group="Выбрать все"):
        """
        Выбирает группу из выпадающего списка.
        :param group: Группа для выбора, по-умолчанию - "Выбрать все".
        """
        self.click_element(self.GROUP_FIELD)
        self.select_dropdown_by_visible_text(self.DROPDOWN_LIST, text=group)


class ProvidersPage(CataloguePage):
    """Страница 'Поставщики' раздела 'Ресурсы'"""

    # ЛОКАТОРЫ ПУНКТОВ МЕНЮ:
    CHECK_CONNECTION = (By.XPATH, '//button[text()="Проверить соединение"]')

    # ЛОКАТОРЫ ФОРМЫ СОЗДАНИЯ ПОСТАВЩИКА:
    NAME = (By.XPATH, '//input[@name="name"]')
    HOST_IP = (By.XPATH, '//input[@name="host"]')
    LOGIN = (By.XPATH, '//input[@name="login"]')
    PASSWORD = (By.XPATH, '//input[@name="password"]')
    HIDE_PASSWORD = (By.XPATH, '//button[@aria-label="toggle password visibility"]')
    ADVANCED_SETTINGS = (By.XPATH, '//button[text()="Расширенные настройки"]')

    # ЛОКАТОРЫ ДОПОЛНИТЕЛЬНЫХ НАСТРОЕК:
    TIMEOUT = (By.XPATH, '//input[@name="timeout"]')
    SSL_CHECKBOX = (By.XPATH, '//span[text()="SSL"]/../span')
    MAX_CREATE_PACKAGE = (By.XPATH, '//input[@name="max_creation_batch_size"]')
    MAX_DELETE_PACKAGE = (By.XPATH, '//input[@name="max_deletion_batch_size"]')

    def __init__(self, driver):
        """
        Инициализирует объект ProvidersPage.
        :param driver: Экземпляр WebDriver.
        """
        super().__init__(driver)

    def create_provider(self, name, host_ip, login, password, advanced_settings=None):
        """
        Создаёт поставщика с переданными параметрами.

        :param name: Имя для поставщика.
        :param host_ip: IP-адрес поставщика.
        :param login: Логин доступа к поставщику.
        :param password: Пароль доступа к поставщику.
        :param advanced_settings: Словарь дополнительных настроек поставщика, по умолчанию - не заданы.
        """
        # Нажать кнопку создать
        self._click_create_button()
        # Заполнение полей поставщика
        self._enter_name(name, clear=False)
        self._enter_host_ip(host_ip)
        self._enter_login(login)
        self._enter_password(password)
        # Дополнительные настройки
        if advanced_settings:
            self._fill_advanced_settings(advanced_settings)
        # Подтверждение создания поставщика
        self._click_form_submit()
        # Проверка нотификации
        self.check_notification("поставщик успешно создан")

    def modify_provider(
        self,
        provider,
        name=None,
        host_ip=None,
        login=None,
        password=None,
        advanced_settings=None,
    ):
        """
        Изменяет параметры существующего поставщика.

        :param provider: Имя существующего поставщика.
        :param name: Новое имя поставщика, по умолчанию - не задано.
        :param host_ip: Новый IP-адрес для поставщика, по умолчанию - не задан.
        :param login: Новый логин для доступа к поставщику, по умолчанию - не задан.
        :param password: Новый пароль для доступа к поставщику, по умолчанию - не задан.
        :param advanced-settings: Словарь новых дополнительных настроек поставщика, по умолчанию - не заданы.
        """
        # Выбор поставщика для изменения
        self.select_row(row=provider)
        # Нажать кнопку "Изменить"
        self._click_edit_button()
        # Изменение параметров поставщика
        if name:
            self._enter_name(name, clear=True)
        if host_ip:
            self._enter_host_ip(host_ip)
        if login:
            self._enter_login(login)
        if password:
            self._enter_password(password)
        if advanced_settings:
            self._fill_advanced_settings(advanced_settings)
        # Подтверждение изменения поставщика
        self._click_form_submit()
        # Проверка нотификации
        self.check_notification("поставщик успешно изменён")

    def delete_provider(self, provider, cancel=False):
        """
        Удаляет поставщика по переданному имени.
        :param provider: Имя поставщика для удаления.
        :param cancel: Флаг отмены удаления, по умолчанию - не отменять.
        """
        # Выбор поставщика для удаления
        self.select_row(row=provider)
        # Нажать кнопку "Удалить"
        self._click_delete_button()
        if cancel:
            # Отмена удаления
            self._click_cancel_delete()
        else:
            # Подтверждение удаления
            self._click_confirm_delete()
            # Проверка нотификации
            self.check_notification("поставщик успешно удалён")

    def check_connection(self, provider, connection="success"):
        """
        Проверяет подключение к поставщику

        :param provider: Имя поставщика для проверки.
        :param connection: Результат проверки подключения, по умолчанию - умпешно.
        """
        # Результаты проверок соединения
        connections = {
            "success": "поставщик успешно проверен",
            "failed": "Не удалось проверить соединение",
        }

        if isinstance(connection, str):
            connection = connections.get(connection)

        # Выбор поставщика для проверки
        self.select_row(row=provider)
        # Нажать кнопку "Проверить соединение"
        self._click_check_connection_button()
        # Проверка нотификации
        self.check_notification(expected_message=connection)

    # Приватные методы:

    def _click_advanced_settings_button(self):
        """Разворачивает дополнительные настройки"""
        self.wait_for_element(self.ADVANCED_SETTINGS, condition="visible")
        self.click_element(self.ADVANCED_SETTINGS)

    def _enter_name(self, name, clear=False):
        """
        Вводит имя поставщика в поле ввода.

        :param name: Имя поставщика.
        :param clear: Флаг для очистки полей ввода, по умолчанию - не очищать.
        """
        self.input_text(*self.NAME, text=name, clear=clear, click=True)

    def _enter_host_ip(self, host_ip):
        """
        Вводит адрес хоста поставщика в поле ввода.
        :param host_ip: IP-адрес хоста поставщика.
        """
        self.input_text(*self.HOST_IP, text=host_ip, clear=True)

    def _enter_login(self, login, clear=False):
        """
        Вводит логин доступа к поставщику в поле ввода.
        
        :param login: Логин.
        :param clear: Флаг для очистки полей ввода, по умолчанию - не очищать.
        """
        self.input_text(*self.LOGIN, text=login, clear=clear, click=False)

    def _enter_password(self, password):
        """
        Вводит пароль доступа к поставщику в поле ввода.
        :param password: Пароль.
        """
        self.input_text(*self.PASSWORD, text=password)

    def _toggle_password_visibility(self):
        """Изменяет отображение пароля"""
        self.click_element(self.HIDE_PASSWORD)

    def _enter_timeout(self, timeout):
        """
        Вводит значение времени ожидания в поле ввода.
        :param timeout: Таймаут ожидания ответа.
        """
        self.input_text(*self.TIMEOUT, text=timeout, clear=True)

    def _click_ssl_checkbox(self):
        """Ставит галку в чекбоксе SSL"""
        self.click_element(self.SSL_CHECKBOX, scroll=True)

    def _enter_max_create_package(self, max_create_package):
        """
        Вводит значение максимального пакета создания в поле ввода.
        :param max_create_package: Размер максимального пакета создания.
        """
        self.click_element(self.MAX_CREATE_PACKAGE, scroll=True)
        self.input_text(
            *self.MAX_CREATE_PACKAGE, text=max_create_package, clear=True, click=False
        )

    def _enter_max_delete_package(self, max_delete_package):
        """
        Вводит значение максимального пакета удаления в поле ввода.
        :param max_create_package: Размер максимального пакета удаления.
        """
        self.click_element(self.MAX_DELETE_PACKAGE, scroll=True)
        self.input_text(
            *self.MAX_DELETE_PACKAGE, text=max_delete_package, clear=True, click=False
        )

    def _fill_advanced_settings(self, advanced_settings):
        """Заполняет все поля дополнительных настроек"""
        # Развернуть дополнительные настройки
        self._click_advanced_settings_button()

        # Получение значений дополнительных настроек
        timeout = advanced_settings.get("timeout", None)
        use_ssl = advanced_settings.get("use_ssl", None)
        max_create_package = advanced_settings.get("max_create_package", None)
        max_delete_package = advanced_settings.get("max_delete_package", None)

        # Заполнение полей
        if timeout:
            self._enter_timeout(timeout)
        if use_ssl:
            self._click_ssl_checkbox()
        if max_create_package:
            self._enter_max_create_package(max_create_package)
        if max_delete_package:
            self._enter_max_create_package(max_delete_package)

    def _click_check_connection_button(self):
        """Инициирует проверку соединения поставщика"""
        self.click_element(self.CHECK_CONNECTION)
