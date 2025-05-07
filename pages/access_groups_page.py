from selenium.webdriver.common.by import By
import pages.catalog_page as cp

# Для метода изменения записи:
import pages.users_page as usp
import pages.groups_page as grp


class AccessGroupsPage(cp.CatalogPage):
    """Страница 'Группы доступа' раздела 'Настройки'"""

    # ЛОКАТОРЫ ПУНКТОВ МЕНЮ
    DETAILS_BUTTON = (By.XPATH, '//button[@data-testid="detail-button"]')
    ADD_BUTTON = (By.XPATH, '//button[text()="Добавить"]')
    ADD_LDAP_BUTTON = (By.XPATH, '//button[text()="Добавить из LDAP"]')
    TAB = (By.XPATH, '//button[text()="{}"]')

    # ЛОКАТОРЫ ФОРМЫ СОЗДАНИЯ ГРУППЫ ДОСТУПА
    NAME = (By.XPATH, '//input[@name="name"]')
    PERMISSIONS_FIELD = (
        By.XPATH, '//div[@id="mui-component-select-template"]')

    # ЛОКАТОРЫ НАСТРОЕК РАЗРЕШЕНИЯ
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

    # ЛОКАТОРЫ ФОРМ ДОБАВЛЕНИЯ
    ADD_FIELD = (By.XPATH, '//div[@id="mui-component-select-entities_ids"]')
    ADD_LDAP_FIELD = (By.XPATH, '//button[@data-cy="form-array-add"]')
    ADD_LDAP_ENTITY = (By.XPATH, '//button[@data-cy="form-array-add"]')
    AUTHENTICATORS_FIELD = (By.XPATH, '//div[@data-cy="auth_strategy_id"]')
    ENTITY_INPUT = (By.XPATH, '//input[@type="text"]')

    # ЛОКАТОРЫ ОКНА ПОДРОБНОЙ ИНФОРМАЦИИ
    EDIT_DETAILS = (By.XPATH, '//button[@data-testid="detail-modal-edit"]')

    # ЛОКАТОРЫ СПИСКА ГРУПП ДОСТУПА
    LAST_CREATED_ACCESS_GROUP_NAME = (
        By.XPATH,
        '//div[@role="rowgroup"]/div[last()]/div[@data-field="name"]',
    )

    def __init__(self, driver):
        """
        Инициализирует объект AccessGroupsPage.
        :param driver: Экземпляр WebDriver.
        """
        super().__init__(driver)

    def create_access_group(self, name, permission, permission_settings=None):
        """
        Создаёт новую группу доступа в системе.

        :param name: Имя для новой группы доступа.
        :param permission: Разрешение группы доступа.
        :param permission_settings: Настройки для разрешения, по умолчанию - не изменять.
        """
        # Нажать кнопку "Создать"
        self.click_create_button()
        # Заполнение полей
        self._enter_name(name)
        self._select_permission(permission)
        if permission_settings:
            # Заполнение полей разрешения
            self._fill_permission_settings(permission_settings)
        # Подтверждение создания
        self.click_form_submit()
        # Проверка нотификации
        self.check_notification("группа доступа успешно создана")
        # ASSERT, проверяющий созданную Группу доступа в списке
        element = self.wait_for_element(
            self.LAST_CREATED_ACCESS_GROUP_NAME, condition="visible"
        )
        assert name == element.text, f"Группа доступа {name} не создана"

    def modify_access_group(
        self, access_group, name=None, permission=None, permission_settings=None
    ):
        """
        Редактирует существуюшую группу доступа.

        :param access_group: Имя существующей группы доступа.
        :param name: Новое имя для группы доступа.
        :param permission: Разрешение группы доступа, по умолчанию - не изменять.
        :param permission_settings: Настройки для разрешения, по умолчанию - не изменять.
        """
        # Выбор группы доступа для редактирования
        self.select_row(access_group)
        # Нажать кнопку "Редактировать"
        self.click_edit_button()
        # Изменение полей
        if name:
            self._enter_name(name, clear=True)
        if permission:
            self._select_permission(permission)
            if permission_settings:
                self._fill_permission_settings(permission_settings)
        # Подтверждение изменений
        self.click_form_submit()
        # Проверка нотификации
        self.check_notification("группа доступа успешно изменена")
        # ASSERT, проверяющий, что редактирование Группы доступа прошли успешно
        element = self.wait_for_element(
            self.LAST_CREATED_ACCESS_GROUP_NAME, condition="visible"
        )
        assert name == element.text, f"Группа доступа {name} не изменена"

    def delete_access_group(self, access_group, cancel=False):
        """
        Удаляет группу доступа по имени.

        :param access_group: Имя группы доступа для удаления.
        :param cancel: Флаг отмены удаления, по умолчанию - не отменять.
        """
        # Выбор группы доступа для удаления
        self.select_row(access_group)
        # Нажать кнопку "Удалить"
        self.click_delete_button()
        if cancel:
            # Отмена удаления
            self.click_cancel_delete()
        else:
            # Подтверждение удаления
            self.click_confirm_delete()
            # Проверка нотификации
            self.check_notification("группа доступа успешно удалена")

    def view_details(self, access_group):
        """
        Открывает страницу дополнительной информации о группе доступа.
        :param access_group: Группа доступа для просмотра доп. инф.
        """
        # Выбор группы доступа
        self.select_row(access_group)
        # Нажать кнопку "Подробнее"
        self._click_details_button()

    def open_tab(self, tab):
        """
        Переключает вкладку страницы дополнительной информации о группе доступа.
        :param tab: Вкладка, на которую производится переключение.
        """
        locator = self.format_xpath(self.TAB, tab)
        self.click_element(locator)

    # TODO: Подумать о другой реализации
    def add_details_entry(self, user=None, group=None):
        """
        Добавляет пользователя / группу в группу доступа.

        :param user: Пользователь для добавления.
        :param group: Группа для добавления.
        """
        if user:
            # Нажать кнопку "Добавить"
            self._click_add_button()
            # Выбор пользователя
            self._select_user(user)
        elif group:
            self.open_tab("Группы")
            # Нажать кнопку "Добавить"
            self._click_add_button()
            # Выбор группы
            self._select_group(group)
        # Подтверждение добавления
        self.click_form_submit()
        # Проверка нотификации
        self.check_notification("сущность успешно добавлена")

    def add_ldap_entity(self, authenticator, ldap_entity):
        """
        Добавляет в группу доступа LDAP-сущность.

        :param authenticator: Аутентификатор, содержащий сущность.
        :param ldap_entity: Имя добавляемой LDAP-сущности.
        """
        # Нажать кнопку "Добавить LDAP-сущность"
        self._click_add_ldap_button()
        # Добавление LDAP-сущности
        self._add_entity(authenticator, ldap_entity)
        # Подтверждение добавления
        self.click_form_submit()
        # Проверка нотификации
        self.check_notification("сущность успешно добавлена")

    def delete_details_entry(self, user=None, group=None, cancel=False):
        """
        Удаляет со страницы дополнительной информации переданную запись.

        :param entry: Запись для удаления (пользователь / группа / LDAP-сущность).
        :param cancel: Флаг отмены удаления, по умолчанию - не отменять.
        """
        # Выбор записи для удаления
        if user:
            self.select_row(user)
        elif group:
            self.select_row(group)
        # Нажать кнопку "Удалить"
        self.click_delete_button()
        if cancel:
            # Отмена удаления
            self.click_cancel_delete()
        else:
            # Подтверждение удаления
            self.click_confirm_delete()
        # Проверка нотификации
        self.check_notification("пользователь успешно удалён")

    def get_entry_details(self, entry):
        """
        Открывает окно подробной информации о записи в списке дополнительной информации о группе доступа.
        :param entry: Запись для получения подробной информации.
        """
        # Выбор записи для получения подробной информации
        self.select_row(entry)
        # Нажать кнопку "Подробнее"
        self._click_details_button()

    def edit_entry_details(self, user=None, group=None):
        """
        Открывает страницу редактирования записи страницы подробной информации о группе доступа.
        :param entry: Запись для редактирования
        """
        # Открыть окно подробной информации о записи
        entry = user or group
        self.get_entry_details(entry)
        # Нажать кнопку "Редактировать"
        self._click_edit_details_button()
        if user:
            users_page = usp.UsersPage(self.driver)
            users_page.modify_user(user=entry, name=entry + "_modified")
        elif group:
            groups_page = grp.GroupsPage(self.driver)
            groups_page.modify_group(group=entry, name=entry + "_modified")

    # Приватные методы:

    def _enter_name(self, name, clear=False):
        """
        Вводит имя группы доступа в поле ввода
        :param name: Имя для группы доступа.
        """
        self.input_text(*self.NAME, text=name, clear=clear, click=True)

    def _select_permission(self, permission):
        """
        Выбирает разрешение из выпадающего списка.
        :param permission: Разрешение.
        """
        self.click_element(self.PERMISSIONS_FIELD)
        self.select_dropdown_by_visible_text(
            self.DROPDOWN_LIST, text=permission)

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

    def _fill_permission_settings(self, settings):
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

    def _click_details_button(self):
        """Открывает страницу дополнительной информации о группе доступа"""
        self.click_element(self.DETAILS_BUTTON)

    def _click_add_button(self):
        """Открывает окно добавления пользователя/группы"""
        self.click_element(self.ADD_BUTTON)

    def _click_add_ldap_button(self):
        """Открывает окно добавления LDAP-сущности"""
        self.click_element(self.ADD_LDAP_BUTTON)

    def _click_add_entity_button(self):
        """Добавляет одну запись в списке добавления LDAP-сущностей"""
        self.click_element(self.ADD_LDAP_ENTITY)

    def _click_edit_details_button(self):
        """"""
        self.click_element(self.EDIT_DETAILS)

    def _select_user(self, user):
        """
        Выбирает пользователя из выпадающего списка.
        :param user: Пользователь к выбору.
        """
        self.wait_for_element(self.ADD_FIELD, condition="visible")
        self.click_element(self.ADD_FIELD)
        self.select_dropdown_by_visible_text(self.DROPDOWN_LIST, text=user)
        self.press_escape()
        self.wait_for_element(self.DROPDOWN_LIST, condition="invisible")

    def _select_group(self, group):
        """
        Выбирает группу из выпадающего списка.
        :param user: Группа к выбору.
        """
        self.wait_for_element(self.ADD_FIELD, condition="visible")
        self.click_element(self.ADD_FIELD)
        self.select_dropdown_by_visible_text(self.DROPDOWN_LIST, text=group)
        self.press_escape()
        self.wait_for_element(self.DROPDOWN_LIST, condition="invisible")

    def _select_authenticator(self, authenticator):
        """
        Выбирает аутентификатор из выпадающего списка.
        :param authenticator: Аутентификатор.
        """
        self.click_element(self.AUTHENTICATORS_FIELD)
        self.select_dropdown_by_visible_text(
            self.DROPDOWN_LIST, text=authenticator)

    def _enter_entity_name(self, entity_name):
        """
        Вводит имя LDAP-сущности в поле ввода.
        :param entity_name: Имя LDAP-сущности.
        """
        self.input_text(*self.ENTITY_INPUT, text=entity_name)

    def _add_entity(self, authenticator, ldap_entity):
        """
        Добавляет одну LDAP-сущность.

        :param authenticator: Аутентификатор с сущностью.
        :param ldap_entity: LDAP-сущность.
        """
        self._click_add_entity_button()
        self._select_authenticator(authenticator)
        self._enter_entity_name(ldap_entity)
