from selenium.webdriver.common.by import By
import pages.catalog_page as cp


class LicensesPage(cp.CatalogPage):
    """Страница 'Лицензии' раздела 'Лицензирование'"""

    # ЛОКАТОРЫ ЛИЦЕНЗИЙ
    LICENSE_ROW_CHECKBOX = (By.XPATH, '//span[text()="{}"]/../../../div[2]')
    TOGGLE_VISIBILITY = (By.XPATH, '//button[@aria-label="toggle password visibility"]')

    # ЛОКАТОР ФОРМЫ ЛИЦЕНЗИОННОГО КЛЮЧА
    LICENSE_KEY = (By.XPATH, '//input[@name="licenseKey"]')

    # ЛОКАТОР КНОПКИ АКТИВАЦИИ ЛИЦЕНЗИЙ
    ACTIVATE_LICENSES_BUTTON = (
        By.XPATH,
        '//button[text()="Активировать лицензии по типу"]',
    )

    # ЛОКАТОРЫ ФОРМЫ АКТИВАЦИИ ЛИЦЕНЗИИ ПО ТИПУ
    REDACTION_TYPE = (By.XPATH, '//div[@data-cy="license-redaction"]')
    LICENSE_TYPE = (By.XPATH, '//div[@data-cy="license-type"]')
    LICENSE_SUBTYPE = (By.XPATH, '//div[@data-cy="license-subtype"]')

    # ЛОКАТОР ЛИЦЕНЗИОННОГО КЛЮЧА
    LICENSE_KEY_NUMBER = (By.XPATH, '//span[text()="{}"]')
    LAST_CREATED_LICENSE_STATUS = (
        By.XPATH,
        '//div[@role="rowgroup"]/div[last()]/div[@data-field="licenseKey"]/../div[8]//*[@data-testid="CheckIcon"]',
    )

    def __init__(self, driver):
        """
        Инициализирует объект LicensesPage.
        :param driver: Экземпляр WebDriver.
        """
        super().__init__(driver)

    def create_license(self, key):
        """Добавляет новую лицензию в систему"""
        # Нажать кнопку "Создать"
        self.click_create_button()
        # Ввод лицензионного ключа
        self._enter_license_key(key)
        # Подтверждение создания лицензии
        self.click_form_submit()
        # Проверка нотификации
        self.check_notification("лицензия успешно создана")
        # Включение видимости всех лицензий
        self._view_licenses()
        # Проверка, что нужная лицензия добавлена
        self.check_result(self.LICENSE_KEY_NUMBER, key, "Лицензия не добавлена")

    def select_license(self, key):
        """Выделяет лицензию по ключу"""
        # Включение видимости всех лицензий
        self._view_licenses()
        # Поиск нужной лицензии по ключу
        locator = self.format_xpath(self.LICENSE_ROW_CHECKBOX, key)
        # Выбор нужной лицензии
        self.set_checkbox(locator)

    def delete_license(self, key, cancel=False):
        """Удаляет лицензию по ключу"""
        # Выбор лицензии для удаления
        self.select_license(key)
        # Нажать кнопку "Удалить"
        self.click_delete_button()
        if cancel:
            # Отменить удаление
            self.click_cancel_delete()
        else:
            # Подтверждение удаления
            self.click_confirm_delete()
            # Проверка нотификации
            self.check_notification("лицензия успешно удалена")

    def activate_license(
        self, redaction_type=None, license_type=None, license_subtype=None
    ):
        """Активирует лицензию по типу"""
        # Нажать кнопку "Активировать лицензии по типу"
        self._click_activate_licenses_button()
        # Выбор лицензий для активации
        if redaction_type:
            self._chose_redaction_type(redaction_type)
        if license_type:
            self._chose_license_type(license_type)
        if license_subtype:
            self._chose_license_subtype(license_subtype)
        # Подтверждение активации
        self.click_form_submit()
        # Проверка нотификаций
        self.check_notification("Лицензии успешно активированы")
        # Проверка, что нужная лицензия активирована
        element = self.wait_for_element(
            self.LAST_CREATED_LICENSE_STATUS, condition="visible"
        )
        # Атрибут data-testid="CheckIcon" обозначает галочку
        assert 'CheckIcon' == element.get_attribute("data-testid"), "Лицензия не активирована"

    # Приватные методы

    def _enter_license_key(self, key):
        """
        Вводит лицензионный ключ в поле ввода.
        :param key: Лицензионный ключ.
        """
        self.input_text(*self.LICENSE_KEY, text=key, click=True)

    def _view_licenses(self):
        """Переключает видимость всех лицензий"""
        elements = self.find_elements(*self.TOGGLE_VISIBILITY)
        for element in elements:
            if element.is_displayed():
                element.click()
            else:
                break

    def _click_activate_licenses_button(self):
        """Инициирует активацию лицензий по типу"""
        self.click_element(self.ACTIVATE_LICENSES_BUTTON)

    def _chose_redaction_type(self, redaction_type):
        """
        Выбирает тип редакции лицензии из выпадающего списка.
        :param redaction_type: Тип редакции.
        """
        self.click_element(self.REDACTION_TYPE)
        self.select_dropdown_by_visible_text(self.DROPDOWN_LIST, text=redaction_type)

    def _chose_license_type(self, license_type):
        """
        Выбирает вид лицензии из выпадающего списка.
        :param license_type: Вид лицензии.
        """
        self.click_element(self.LICENSE_TYPE)
        self.select_dropdown_by_visible_text(self.DROPDOWN_LIST, text=license_type)

    def _chose_license_subtype(self, license_subtype):
        """
        Выбирает тип лицензии из выпадающего списка.
        :param redaction_type: Тип лицензии.
        """
        self.click_element(self.LICENSE_SUBTYPE)
        self.select_dropdown_by_visible_text(self.DROPDOWN_LIST, text=license_subtype)
