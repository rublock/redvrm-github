from selenium.webdriver.common.by import By
import pages.catalog_page as cp


class AuthenticatorsPage(cp.CatalogPage):
    """Страница 'Аутентификаторы' раздела 'Учётные записи'"""

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
    HIDE_PASSWORD = (
        By.XPATH, '//button[@aria-label="toggle password visibility"]')
    ADVANCED_SETTINGS = (By.XPATH, '//button[text()="Расширенные настройки"]')

    # ЛОКАТОРЫ ДОПОЛНИТЕЛЬНЫХ НАСТРОЕК:
    AUTHORITY = (By.XPATH, '//input[@name="settings.ldap_base"]')
    TIMEOUT = (By.XPATH, '//input[@name="settings.connection_timeout"]')
    SSL_CHECKBOX = (By.XPATH, '//span[text()="использовать SSL"]/../span')
    USER_CLASS = (By.XPATH, '//input[@name="settings.ldap_user_class"]')
    ID_ATTRIBUTE = (By.XPATH, '//input[@name="settings.ldap_user_id_attr"]')
    USER_ATTRIBUTE = (By.XPATH, '//input[@name="settings.ldap_username_attr"]')
    GROUP_ATTRIBUTE = (
        By.XPATH, '//input[@name="settings.ldap_groupname_attr"]')
    ALTERNATIVE_CLASS = (
        By.XPATH, '//input[@name="settings.alternative_class"]')

    # ЛОКАТОРЫ СПИСКА АУТЕНТИФИКАТОРОВ:
    LAST_CREATED_AUTHENTICATOR_NAME = (
        By.XPATH,
        '//div[@role="rowgroup"]/div[last()]/div[@data-field="auth_name"]',
    )

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
        self.click_create_button()
        # Заполнение полей аутентификатора
        self._enter_name(name)
        self._enter_description(description)
        self._select_type(auth_type)
        # Дополнительные настройки
        self._fill_auth_settings(auth_type, auth_settings)
        # Подтверждение создания аутентификатора
        self.click_form_submit()
        # Проверка нотификации
        self.check_notification("аутентификатор успешно создан")
        # Проверка, что аутентификатор успешно создан
        self.check_result(
            self.LAST_CREATED_AUTHENTICATOR_NAME,
            name,
            f"Аутентификатор {name} не создан"
        )

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
        self.click_edit_button()
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
        self.click_form_submit()
        # Проверка нотификации
        self.check_notification("аутентификатор успешно изменён")
        # Проверка, что аутентификатор успешно изменен
        element = self.wait_for_element(
            self.LAST_CREATED_AUTHENTICATOR_NAME, condition="visible"
        )
        assert name == element.text, f"Аутентификатор {name} не изменен"

    def delete_authenticator(self, authenticator, cancel=False):
        """
        Удаляет аутентификатор по переданному имени.

        :param name: Имя для аутентификатора к удалению.
        :param cancel: Флаг отмены удаления, по умолчанию - не отменять.
        """
        # Выбрать аутентификатор для удаления
        self.select_row(row=authenticator)
        # Нажать кнопку "Удалить"
        self.click_delete_button()
        if cancel:
            # Отмена удаления
            self.click_cancel_delete()
        else:
            # Подтверждение удаления
            self.click_confirm_delete()
            # Проверка нотификации
            self.check_notification("аутентификатор успешно удалён")
            # Проверка, что аутентификатор успешно удален
            element = self.wait_for_element(
                self.LAST_CREATED_AUTHENTICATOR_NAME, condition="visible"
            )
            assert (
                authenticator != element.text
            ), f"Аутентификатор {authenticator} не удален"

    def check_connection(self, authenticator, connection="success"):
        """
        Проверяет соединение выбранного аутентификатора.

        :param authenticator: Аутентификатор для проверки.
        :param connection: Результат проверки подключения, по умолчанию - успешно.
        """
        # Результаты проверок
        connections = {
            "success": "аутентификатор успешно проверен",
            "failed": "Не удалось установить соединение",
        }

        if isinstance(connection, str):
            connection = connections.get(connection)

        # Выбор аутентификатора для проверки
        self.select_row(row=authenticator)
        # Нажать кнопку проверить соединение
        self._click_check_connection_button()
        # Проверить нотификацию
        self.check_notification(expected_message=connection)

    # Приватные методы:

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
        self.input_text(*self.DESCRIPTION, text=description,
                        clear=clear, click=True)

    def _select_type(self, auth_type):
        """
        Выбирает тип аутентификатора из выпадающего списка.
        :param auth_type: Тип аутентификатора для выбора.
        """
        self.click_element(self.AUTH_TYPE_FIELD)
        self.select_dropdown_by_visible_text(
            self.DROPDOWN_LIST, text=auth_type)

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
        self.input_text(*self.AUTHORITY, text=authority,
                        clear=clear, click=False)

    def _enter_timeout(self, timeout):
        """
        Вводит значение времени ожидания в поле ввода.
        :param timeout: Таймаут ожидания ответа.
        """
        self.click_element(self.TIMEOUT, scroll=True)
        self.input_text(*self.TIMEOUT, text=timeout, clear=True, click=False)

    def _click_ssl_checkbox(self):
        """Ставит галку в чекбоксе SSL"""
        self.scroll_to_element(self.SSL_CHECKBOX)
        self.set_checkbox(self.SSL_CHECKBOX, state=True)

    def _enter_user_class(self, user_class):
        """
        Вводит пользовательский класс в поле ввода.
        :param user_class: Пользовательский класс.
        """
        self.click_element(self.USER_CLASS, scroll=True)
        self.input_text(*self.USER_CLASS, text=user_class,
                        clear=True, click=False)

    def _enter_id_attribute(self, id_attribute):
        """
        Вводит атрибут ID в поле ввода.
        :param id_attribute: ID-атрибут.
        """
        self.click_element(self.ID_ATTRIBUTE, scroll=True)
        self.input_text(*self.ID_ATTRIBUTE, text=id_attribute,
                        clear=True, click=False)

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
