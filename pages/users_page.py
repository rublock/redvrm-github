

from selenium.webdriver.common.by import By
import pages.catalog_page as cp


class UsersPage(cp.CatalogPage):
    """Страница 'Пользователи' раздела 'Учётные записи'"""

    # ЛОКАТОРЫ ПУНКТОВ МЕНЮ
    BLOCK_BUTTON = (By.XPATH, '//button[text()="Заблокировать"]')

    # ЛОКАТОРЫ ФОРМЫ СОЗДАНИЯ ПОЛЬЗОВАТЕЛЯ:
    AUTHENTICATORS_FIELD = (By.XPATH, '//input[@name="auth_strategy"]/../div')
    NAME_FIELD = (By.XPATH, '//input[@name="name"]')
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
            name,
            password,
            show_password=False,
            role="Пользователь",
            group=None,
            error_name=None,
    ):
        """
        Создаёт нового пользователя с переданными параметрами.

        :param authenticator: Аутентификатор.
        :param name: Имя пользователя.
        :param password: Пароль пользователя.
        :param show_password: Флаг установки видимости пароля, по умолчанию - не показывать.
        :param role: Роль, по-умолчанию - "Пользователь".
        :param group: Группа для выбора, по умолчанию - не задана.
        :param error_name: Имя ошибки для assert

        """
        # Открыть окно создания пользователя
        self.click_create_button()
        # Выбор аутентификатора
        self._select_authenticator(authenticator)
        # Ввод данных пользователя
        self._enter_name(name, clear=False)
        if show_password:
            self._toggle_password_visibility()
        self._enter_password(password)
        # Выбор роли
        self._select_role(role)
        # Выбор группы
        if group:
            self._select_group(group)
        # Завершить создание пользователя
        self.click_form_submit()

        #Заменить текст на актуальный, когда пофиксят баг
        if error_name == 'validation':
            self.check_notification('Заполните поле пароль')
        elif error_name == 'duplicate':
            self.check_notification(
                'Ошибка: {"non_field_errors":["The fields name, auth_strategy must make a unique set."]}'
            )
        else:
            self.check_notification("пользователь успешно создан")

    def modify_user(
        self,
        user,
        authenticator=None,
        name=None,
        password=None,
        show_password=False,
        role=None,
        group=None,
    ):
        """
        Изменяет параметры существующего пользователя.

        :param user: Имя существующего пользователя для изменения.
        :param authenticator: Новый аутентификатор, по умолчанию - не изменяется.
        :param name: Новый логин пользователя, по умолчанию - не изменяется.
        :param password: Новый пароль пользователя, по умолчанию - не изменяется.
        :param show_password: Флаг установки видимости пароля, по умолчанию - не показывать.
        :param role: Новая роль для пользователя, по умолчанию - не изменяется.
        :param group: Новая группа для пользователя, по умолчанию - не изменяется.
        """
        # Выбор пользователя для изменения
        self.select_row(user)
        # Открыть окно изменения пользователя
        self.click_edit_button()
        # Изменение параметров
        if authenticator:
            self._select_authenticator(authenticator)
        if name:
            self._enter_name(name, clear=True)
        if password:
            if show_password:
                self._toggle_password_visibility()
            self._enter_password(password)
        if role:
            self._select_role(role)
        if group:
            self._select_group(group)
        # Завершить редактирование пользователя
        self.click_form_submit()
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
        self.click_delete_button()
        if cancel:
            # Отмена удаления
            self.click_cancel_delete()
        else:
            # Подтверждение удаления
            self.click_confirm_delete()
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

    def _enter_name(self, name, clear=False):
        """
        Вводит имя пользователя в поле ввода имени пользователя.

        :param name: Имя пользователя для ввода.
        :param clear: Флаг для очистки полей ввода, по умолчанию - не очищать.
        """
        self.input_text(*self.NAME_FIELD, text=name, clear=clear, click=True)

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
