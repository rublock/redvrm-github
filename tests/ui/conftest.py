import pytest

# ДЛЯ РАБОТЫ WEBDRIVER
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# БАЗОВЫЕ СТРАНИЦЫ
# from pages.base import BasePage
import pages.login_page as lp
import pages.catalog_page as cp

# СТРАНИЦЫ РАЗДЕЛА "УЧЁТНЫЕ ЗАПИСИ"
import pages.authenticators_page as aup
import pages.groups_page as grp
import pages.users_page as usp

# СТРАНИЦЫ РАЗДЕЛА "РЕСУРСЫ"
import pages.agents_page as asp
import pages.providers_page as prp

# СТРАНИЦЫ РАЗДЕЛА "ЛИЦЕНЗИРОВАНИЕ"
import pages.licenses_page as lsp

# СТРАНИЦЫ РАЗДЕЛА "НАСТРОЙКИ"
import pages.permissions_page as psp
import pages.access_groups_page as agp


@pytest.fixture(scope="function")
def driver():
    "Инициализация WebDriver перед тестами и его завершение после"
    chrome_options = Options()
    chrome_options.add_argument("--force-device-scale-factor=1") # Регулировка масштаба
    chrome_options.add_argument("--high-dpi-support=1")
    dr = Chrome(service=Service(), options=chrome_options)
    dr.maximize_window()
    yield dr
    dr.quit()


@pytest.fixture
def login_admin(login_page):
    """Авторизация администратора"""
    login_page.login_admin()


# TODO: Фикстура открытия страницы (autouse).
# В тестах сделать открываемую страницу аттрибутом.
# @pytest.fixture(autouse=True)
# def open_page(origin_page, destination_page):
#     """
#     Открывает страницу назначения, находясь на изначально странице.
#     Пример использования: @pytest.mark.parametrize("open_page", f"{self.PAGE}", indirect=True)

#     :param origin_page: Страница, с которой осуществляется переход.
#     :param destination_page: Страница, на которую осуществляется переход.
#     """
#     origin_page.open_page(destination_page)


@pytest.fixture
def login_page(driver):
    """Создаёт экземпляр страницы авторизации"""
    return lp.LoginPage(driver)


@pytest.fixture
def catalogue_page(driver):
    """Создаёт экземпляр страницы-каталога"""
    page = cp.CatalogPage(driver)
    # page.open_page(page.PAGES["users"])
    return page


@pytest.fixture
def authenticators_page(driver):
    """Создаёт экземпляр страницы аутентификаторов"""
    page = aup.AuthenticatorsPage(driver)
    # page.open_page(page.PAGES["authenticators"])
    return page


@pytest.fixture
def groups_page(driver):
    """Создаёт экземпляр страницы групп"""
    page = grp.GroupsPage(driver)
    # page.open_page(page.PAGES["groups"])
    return page


@pytest.fixture
def users_page(driver):
    """Создаёт экземпляр страницы пользователей"""
    page = usp.UsersPage(driver)
    # page.open_page(page.PAGES["users"])
    return page


@pytest.fixture
def agents_page(driver):
    """Создаёт экземпляр страницы агентов"""
    page = asp.AgentsPage(driver)
    # page.open_page(page.PAGES["agents"])
    return page


@pytest.fixture
def providers_page(driver):
    """Создаёт экземпляр страницы провайдеров"""
    page = prp.ProvidersPage(driver)
    # page.open_page(page.PAGES["providers"])
    return page


@pytest.fixture
def licenses_page(driver):
    """Создаёт экземпляр страницы лицензий"""
    page = lsp.LicensesPage(driver)
    # page.open_page(page.PAGES["licenses"])
    return page


@pytest.fixture
def permissions_page(driver):
    """Создаёт экземпляр страницы разрешений"""
    page = psp.PermissionsPage(driver)
    # page.open_page(page.PAGES["permissions"])
    return page


@pytest.fixture
def access_groups_page(driver):
    """Создаёт экземпляр страницы групп доступа"""
    page = agp.AccessGroupsPage(driver)
    # page.open_page(page.PAGES["access_groups"])
    return page
