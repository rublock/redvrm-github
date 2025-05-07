from selenium.webdriver.common.by import By
import pages.base_page as bp


class UserPage(bp.BasePage):
    """
    Страница пользователя РЕД ВРМ.
    """

    # ЛОКАТОРЫ:
    ADMIN_PAGE_BUTTON = (By.CSS_SELECTOR, "button:nth-child(5)")
    THEME_SWITCH_BUTTON = (By.XPATH, '//div[@data-testid="theme-switch-button"]')
    ABOUT_BUTTON = (By.XPATH, '//div[@data-testid="info-button"]')

    def __init__(self, driver):
        """
        Инициализирует объект UserPage.
        :param driver: Экземпляр WebDriver.
        """
        super().__init__(driver)

    def click_admin_page(self):
        """Переходит на страницу администратора из меню пользователя"""
        self.click_element(self.ADMIN_PAGE_BUTTON)

    def switch_theme(self):
        """Переключает тему оформления системы"""
        self.click_element(self.THEME_SWITCH_BUTTON)

    def view_about(self):
        """Открывает информацию о системе"""
        self.click_element(self.ABOUT_BUTTON)
