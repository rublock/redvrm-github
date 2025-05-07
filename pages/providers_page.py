from selenium.webdriver.common.by import By
import pages.catalog_page as cp


class ProvidersPage(cp.CatalogPage):
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
    # ЛОКАТОРЫ СПИСКА ПОСТАВЩИКОВ
    LAST_CREATED_PROVIDERS_NAME = (
        By.XPATH,
        '//div[@role="rowgroup"]/div[last()]/div[@data-field="name"]',
    )

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
        self.click_create_button()
        # Заполнение полей поставщика
        self._enter_name(name, clear=False)
        self._enter_host_ip(host_ip)
        self._enter_login(login)
        self._enter_password(password)
        # Дополнительные настройки
        if advanced_settings:
            self._fill_advanced_settings(advanced_settings)
        # Подтверждение создания поставщика
        self.click_form_submit()
        # Проверка нотификации
        self.check_notification("поставщик успешно создан")
        # ASSERT, проверяющий созданного Поставщика в списке
        element = self.wait_for_element(
            self.LAST_CREATED_PROVIDERS_NAME, condition="visible"
        )
        assert name == element.text, f"Поставщик {name} не создан"

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
        self.click_edit_button()
        # Изменение параметров поставщика
        if name:
            self._enter_name(name, clear=True)
        if host_ip:
            self._enter_host_ip(host_ip)
        if login:
            self._enter_login(login, clear=True)
        if password:
            self._enter_password(password)
        if advanced_settings:
            self._fill_advanced_settings(advanced_settings)
        # Подтверждение изменения поставщика
        self.click_form_submit()
        # Проверка нотификации
        self.check_notification("поставщик успешно изменён")
        # ASSERT, проверяющий созданного Поставщика в списке
        element = self.wait_for_element(
            self.LAST_CREATED_PROVIDERS_NAME, condition="visible"
        )
        assert name == element.text, f"Поставщик {name} не изменён"

    def delete_provider(self, provider, cancel=False):
        """
        Удаляет поставщика по переданному имени.
        :param provider: Имя поставщика для удаления.
        :param cancel: Флаг отмены удаления, по умолчанию - не отменять.
        """
        # Выбор поставщика для удаления
        self.select_row(row=provider)
        # Нажать кнопку "Удалить"
        self.click_delete_button()
        if cancel:
            # Отмена удаления
            self.click_cancel_delete()
        else:
            # Подтверждение удаления
            self.click_confirm_delete()
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
            self._enter_max_delete_package(max_delete_package)

    def _click_check_connection_button(self):
        """Инициирует проверку соединения поставщика"""
        self.click_element(self.CHECK_CONNECTION)
