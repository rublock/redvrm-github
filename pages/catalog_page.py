from selenium.webdriver.common.by import By
import pages.base_page as bp
import pages.config_redvrm as config_redvrm


class CatalogPage(bp.BasePage):
    """
    Базовый класс для страниц, содержащих каталоги.
    Обеспечивает методы для работы с каталогами.
    """

    SECTIONS = config_redvrm.SECTIONS
    PAGES = config_redvrm.PAGES

    # ЛОКАТОРЫ МЕНЮ СИСТЕМЫ:
    MENU_ENTRY = (By.XPATH, '//span[text()="{}"]/../../..')
    ABOUT = (By.XPATH, '//div[@data-testid="sidebar-about"]')
    LOGOUT = (By.XPATH, '//button[@aria-label="Выйти"]')

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
    HEADER = (By.XPATH, '//h1[text()="{}"]')
    # COLUMNS_HEADERS = (By.XPATH, '//div[@role="columnheader"]')
    ROWS = (By.XPATH, '//div[@role="rowgroup"]')
    ROW = (By.XPATH, '//div[text()="{}"]/../div[2]')
    CHOOSE_ALL_CHECKBOX = (By.XPATH, "//input[@aria-label='Выбрать все строки']/..")
    DROPDOWN_LIST = (By.XPATH, '//ul[@role="listbox"]/li')

    # ЛОКАТОРЫ ДЕЙСТВИЙ ФОРМ
    FORM_SUBMIT = (By.XPATH, '//button[@data-testid="form-drawer-submit"]')
    FORM_CLOSE = (By.XPATH, '//button[@aria-label="Закрыть"]')

    # ЛОКАТОРЫ ПОДТВЕРЖДЕНИЯ УДАЛЕНИЯ
    CANCEL_DELETE = (By.XPATH, '//div[@role="dialog"]/div[2]/div[1]')
    CONFIRM_DELETE = (By.XPATH, '//div[@role="dialog"]/div[2]/div[2]')

    # ЛОКАТОРЫ СТРОКИ СОСТОЯНИЯ
    SELECT_ALL = (By.XPATH, '//input[@aria-label="Выбрать все строки"]')
    STRINGS_ON_PAGE = (By.XPATH, '//div[@aria-haspopup="listbox"]')
    PREVIOUS_BUTTON = (By.XPATH, '//div[@class="MuiTablePagination-actions"]/button[1]')
    NEXT_BUTTON = (By.XPATH, '//div[@class="MuiTablePagination-actions"]/button[2]')

    def __init__(self, driver):
        """
        Инициализирует объект CataloguePage.
        :param driver: Экземпляр WebDriver.
        """
        self.BASE_URL = self.BASE_URL + "admin"
        super().__init__(driver)

    def click_create_button(self):
        """Открывает модальное окно создания пользователя"""
        self.click_element(self.CREATE_BUTTON)
        self.wait_for_element(self.FORM_SUBMIT)

    def click_edit_button(self):
        """Открывает модальное окно изменения пользователя"""
        self.click_element(self.EDIT_BUTTON)
        self.wait_for_element(self.FORM_SUBMIT)

    def click_delete_button(self):
        """Инициирует удаление пользователя"""
        self.click_element(self.DELETE_BUTTON)
        self.wait_for_element(self.CONFIRM_DELETE)

    def click_form_submit(self):
        """Закрывает модальное окно, завершая действие"""
        self.click_element(self.FORM_SUBMIT)

    def click_form_close(self):
        """Закрывает модальное окно, отменяя действие"""
        self.click_element(self.FORM_CLOSE)

    def click_confirm_delete(self):
        """Подтверждает удаление записи из каталога"""
        self.click_element(self.CONFIRM_DELETE)

    def click_cancel_delete(self):
        """Отменяет удаление записи в каталоге"""
        self.click_element(self.CANCEL_DELETE)

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
        Выбирает переданную запись.
        :param row: Запись для удаления.
        """
        self.wait_for_element(self.ROWS, condition="visible")
        locator = self.format_xpath(self.ROW, row)
        self.click_element(locator)

    def select_rows(self, rows):
        """
        Выбирает переданные строки из списка страницы-каталога.
        """
        for row in rows:
            self.select_row(row)

    def open_page(self, page):
        """
        Открывает страницу из левого меню системы.
        :param page: Открываемая страница.
        """
        # Выбор нужного раздела
        page_names = list(self.PAGES)
        if page in [self.PAGES[page_name] for page_name in page_names[0:3]]:
            self._unfold_section(self.SECTIONS["credentials"])
        elif page in [self.PAGES[page_name] for page_name in page_names[3:6]]:
            self._unfold_section(self.SECTIONS["resources"])
        elif page in [self.PAGES[page_name] for page_name in page_names[7:9]]:
            self._unfold_section(self.SECTIONS["licensing"])
        elif page in [self.PAGES[page_name] for page_name in page_names[9:11]]:
            self._unfold_section(self.SECTIONS["options"])

        # Переход на страницу
        locator = self.format_xpath(self.MENU_ENTRY, page)
        self.click_element(locator)

        locator = self.format_xpath(self.HEADER, page)
        self.wait_for_element(locator)

    def logout(self):
        """Выполняет выход из системы"""
        self.click_element(self.LOGOUT)

    def view_about(self):
        """Показывает информацию о системе из левого меню"""
        self.click_element(self.ABOUT)

    # Приватные методы:

    def _unfold_section(self, section):
        """
        Разворачивает раздел в левом меню системы.
        :param section: Разворачиваемый раздел.
        """
        locator = self.format_xpath(self.MENU_ENTRY, section)
        self.click_element(locator)

    def _click_columns_button(self):
        """Открывает меню выбора столбцов для показа"""
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
        self._select_column("Show/Hide All")
