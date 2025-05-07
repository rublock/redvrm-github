from selenium.webdriver.common.by import By
import pages.catalog_page as cp


class PermissionsPage(cp.CatalogPage):
    """Страница 'Разрешения' раздела 'Настройки'"""

    # ЛОКАТОРЫ ФОРМЫ СОЗДАНИЯ РАЗРЕШЕНИЯ
    NAME = (By.XPATH, '//input[@name="name"]')
    PORT = (By.XPATH, '//input[@name="data.port"]')
    FULLSCREEN = (By.XPATH, '//span[text()="Во весь экран"]/../span[1]')
    LOGIN = (By.XPATH, '//input[@name="data.login"]')
    PASSWORD_VISIBILITY = (
        By.XPATH,
        '//button[@aria-label="toggle password visibility"]',
    )
    PASSWORD = (By.XPATH, '//input[@name="data.password"]')
    WIDTH = (By.XPATH, '//input[@name="data.width"]')
    HEIGH = (By.XPATH, '//input[@name="data.height"]')
    DYNAMIC_RESOLUTION = (
        By.XPATH,
        '//span[text()="Динамическое разрешение"]/../span[1]',
    )
    CLIPBOARD = (By.XPATH, '//span[text()="Буфер обмена"]/../span[1]')
    SMART_CARD = (By.XPATH, '//span[text()="Смарт карта"]/../span[1]')

    # ЛОКАТОР НАЗВАНИЕ ПОСЛЕДНЕГО СОЗДАННОГО РАЗРЕШЕНИЯ
    LAST_CREATED_PERMISSION_NAME = (
        By.XPATH,
        '//div[@role="rowgroup"]/div[last()]/div[@data-field="name"]',
    )

    def __init__(self, driver):
        """
        Инициализирует объект PermissionsPage.
        :param driver: Экземпляр WebDriver.
        """
        super().__init__(driver)

    def create_permission(self, name, settings=None):
        """
        Добавляет новое разрешение в систему.

        :param name: Имя разрешения.
        :param settings: Словарь настроек разрешения, по умолчанию - системные настройки.
        """
        # Нажать кнопку "Создать"
        self.click_create_button()
        # Заполнение полей
        self._enter_name(name, clear=False)
        self._fill_settings(settings)
        # Подтверждение создания
        self.click_form_submit()
        # Проверка нотификации
        self.check_notification("разрешение успешно создано")
        # ASSERT, проверяющий созданное Разрешение в списке
        element = self.wait_for_element(
            self.LAST_CREATED_PERMISSION_NAME, condition="visible"
        )
        assert name == element.text, f"Разрешение {name} не создано"

    def modify_permission(self, permission, name=None, settings=None):
        """
        Изменяет параметры существующего разрешения.

        :param permission: Имя разрешения для изменения.
        :param name: Новое имя для разрешения, по умолчанию - Не изменять.
        :param settings: Словарь новых настроек разрешения, по умолчанию - не изменять.
        """
        # Выбор разрешения для изменения
        self.select_row(permission)
        # Нажать кнопку "Редактировать"
        self.click_edit_button()
        # Изменение полей
        if name:
            self._enter_name(name, clear=True)
        if settings:
            self._fill_settings(settings)
        # Подтверждение изменений
        self.click_form_submit()
        # Проверка нотификации
        self.check_notification("разрешение успешно изменено")
        # ASSERT, проверяющий созданное Разрешение в списке
        element = self.wait_for_element(
            self.LAST_CREATED_PERMISSION_NAME, condition="visible"
        )
        assert name == element.text, f"Разрешение {name} не изменено"

    def delete_permission(self, permission, cancel=False):
        """
        Удаляет разрешение из системы.

        :param permission: Имя разрешения для удаления.
        :param cancel: Флаг отмены удаления, по умолчанию - удалить.
        """
        # Выбор разрешения для удаления
        self.select_row(permission)
        # Нажать кнопку "Удалить"
        self.click_delete_button()
        if cancel:
            # Отменить удаление
            self.click_cancel_delete()
        else:
            # Подтвердить удаление
            self.click_confirm_delete()
            #  Проверка нотификации
            self.check_notification("разрешение успешно удалено")

    # Приватные методы:

    def _enter_name(self, name, clear=False):
        """
        Вводит имя разрешения в поле ввода
        :param name: Имя разрешения.
        """
        self.input_text(*self.NAME, text=name, clear=clear, click=True)

    def _enter_port(self, port):
        """
        Вводит порт подключения в поле ввода.
        :param port: Порт.
        """
        self.input_text(*self.PORT, text=port)

    def _click_fullscreen_checkbox(self, state):
        """Переключает чекбокс разрешения полного экрана"""
        self.set_checkbox(self.FULLSCREEN, state=state)

    def _enter_login(self, login):
        """
        Вводит логин доступа в поле ввода.
        :param login: Логин.
        """
        self.input_text(*self.LOGIN, text=login, click=True)

    def _toggle_password_visibility(self):
        """Изменяет отображение пароля"""
        self.click_element(self.PASSWORD_VISIBILITY)

    def _enter_password(self, password):
        """
        Вводит пароль досутпа в поле ввода.
        :param password: Пароль.
        """
        self._toggle_password_visibility()
        self.input_text(*self.PASSWORD, text=password, click=True)

    def _enter_width(self, width):
        """
        Вводит ширину окна в поле для ввода.
        :param width: Ширина окна.
        """
        self.input_text(*self.WIDTH, text=width, click=True)

    def _enter_heigh(self, heigh):
        """
        Вводит высоту окна в поле для ввода.
        :param heigh: Высота окна.
        """
        self.input_text(*self.HEIGH, text=heigh, click=True)

    def _click_dynamic_resolution_checkbox(self, state):
        """Переключает чекбокс динамического разрешения"""
        self.scroll_to_element(self.DYNAMIC_RESOLUTION)
        self.set_checkbox(self.DYNAMIC_RESOLUTION, state)

    def _click_clipboard_checkbox(self, state):
        """Переключает чекбокс буфера обмена"""
        self.scroll_to_element(self.CLIPBOARD)
        self.set_checkbox(self.CLIPBOARD, state)

    def _click_smart_card_checkbox(self, state):
        """Переключает чекбокс использования смарт карты"""
        self.scroll_to_element(self.SMART_CARD)
        self.set_checkbox(self.SMART_CARD, state)

    def _fill_settings(self, settings):
        """Заполняет все поля настроек разрешения"""
        # Получение значений настроек
        port = settings.get("port", None)
        fullscreen = settings.get("fullscreen", None)
        login = settings.get("login", None)
        password = settings.get("password", None)
        width = settings.get("width", None)
        heigh = settings.get("heigh", None)
        dynamic_resolution = settings.get("dynamic_resolution", None)
        clipboard = settings.get("clipboard", None)
        smart_card = settings.get("smart_card", None)

        # Заполнение полей
        if port:
            self._enter_port(port)
        if fullscreen is not None:
            self._click_fullscreen_checkbox(fullscreen)
        if login:
            self._enter_login(login)
        if password:
            self._enter_password(password)
        if width:
            self._enter_width(width)
        if heigh:
            self._enter_heigh(heigh)
        if dynamic_resolution is not None:
            self._click_dynamic_resolution_checkbox(dynamic_resolution)
        if clipboard is not None:
            self._click_clipboard_checkbox(clipboard)
        if smart_card is not None:
            self._click_smart_card_checkbox(smart_card)
