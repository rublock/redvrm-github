from selenium.webdriver.common.by import By
import pages.catalog_page as cp


class GroupsPage(cp.CatalogPage):
    """Страница 'Группы' раздела 'Учетные записи'"""

    # ЛОКАТОРЫ ПУНКТОВ МЕНЮ:
    DETAILS_BUTTON = (By.XPATH, "//button[@data-testid='detail-button']")
    ADD_BUTTON = (By.XPATH, '//button[text()="Добавить"]')

    # ЛОКАТОРЫ ФОРМЫ СОЗДАНИЯ ГРУППЫ:
    NAME_INPUT = (By.XPATH, '//input[@name="name"]')

    # ЛОКАТОРЫ ФОРМЫ ДОБАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯ:
    ADD_FIELD = (By.XPATH, '//div[@id="mui-component-select-user_ids"]')

    # ЛОКАТОРЫ СПИСКА ГРУПП:
    LAST_CREATED_GROUP_NAME = (
        By.XPATH,
        '//div[@role="rowgroup"]/div[last()]/div[@data-field="name"]',
    )
    ALL_GROUPS_NAMES = (By.XPATH, "//div[@data-field='name']")

    # ЛОКАТОР ДЛЯ КЛИКА ПО ВСЕМУ ЭКРАНА
    ALL_WINDOW = (
        By.XPATH, '//div[contains(@class, "MuiBackdrop-root") and contains(@class, "MuiBackdrop-invisible")]')

    def __init__(self, driver):
        """
        Инициализирует объект GroupsPage.
        :param driver: Экземпляр WebDriver.
        """
        super().__init__(driver)

    def create_group(self, name):
        """
        Создаёт новую группу с переданными параметрами.
        :param name: Имя для новой группы.
        """
        self.click_create_button()
        self._enter_name(name)
        self.click_form_submit()
        # Проверка нотификации
        self.check_notification("группа успешно создана")
        # Проверка, что аутентификатор успешно изменен
        element = self.wait_for_element(
            self.LAST_CREATED_GROUP_NAME, condition="visible"
        )
        assert name == element.text, f"Группа {name} не создана"

    def modify_group(self, group, name=None):
        """
        Изменяет параметры существующей группы.

        :param group: Имя группы для изменения.
        :param name: Новое имя для группы.
        """
        self.select_row(group)
        self.click_edit_button()
        self._enter_name(name)
        self.click_form_submit()
        # Проверка нотификации
        self.check_notification("группа успешно изменена")
        # Проверка, что группа успешно изменена
        element = self.wait_for_element(
            self.LAST_CREATED_GROUP_NAME, condition="visible"
        )
        assert name == element.text, f"Группа {name} не изменена"

    def delete_group(self, group, cancel=False):
        """
        Удаляет группу по переданному имени.

        :param group_name: Имя для группы к удалению.
        :param cancel: Флаг отмены удаления, по умолчанию - не отменять.
        """
        # Выбрать группу для удаления
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
            self.check_notification("группа успешно удалена")
            # Проверка, что группа успешно удалена
            all_groups = self.driver.find_elements(*self.ALL_GROUPS_NAMES)
            groups_names = [group.text for group in all_groups]
            assert group not in groups_names, f"Группа {group} не удалена. Остались группы: {groups_names}"

    def add_user(self, group, user):
        """
        Добавляет пользователя в группу.

        :param group: Группа, в которую добавляется пользователь.
        :param user: Пользователь для добавления.
        """
        # Выбор группы
        self.select_row(group)
        # Нажать кнопку "Подробнее"
        self._click_details_button()
        # Нажать кнопку "Добавить"
        self._click_add_button()
        # Выбор пользователя
        self._select_user(user)
        # Подтверждение добавления
        self.click_form_submit()
        # Проверка нотификации
        self.check_notification("пользователь успешно добавлен")

    # Приватные методы:

    def _enter_name(self, name=None):
        """
        Заполняет форму для созднания группы.
        :param name: имя группы.
        """
        self.input_text(*self.NAME_INPUT, text=name)

    def _click_details_button(self):
        """Открывает страицу дополнительной информации о группе"""
        self.click_element(self.DETAILS_BUTTON)

    def _click_add_button(self):
        """Открывает окно добавления пользователя/группы"""
        self.click_element(self.ADD_BUTTON)

    def _select_user(self, user):
        """Выбирает пользователя из выпадающего списка"""
        self.wait_for_element(self.ADD_FIELD, condition="clickable")
        self.click_element(self.ADD_FIELD)
        self.select_dropdown_by_visible_text(self.DROPDOWN_LIST, text=user)
        self.press_escape()
        self.wait_for_element(self.DROPDOWN_LIST, condition="invisible")
