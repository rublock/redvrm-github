import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



@pytest.mark.usefixtures("login_admin")
class TestCatalogue:
    """Тесты  для страниц-каталогов"""

    def test_select_column(self, catalogue_page):
        """Проверяет возможность выбора столбца для отображения"""
        with allure.step("Выбор столбца ID"):
            catalogue_page.show_column("ID")

            allure.attach(
                catalogue_page.driver.get_screenshot_as_png(),
                name="Столбец ID отображён.",
                attachment_type=allure.attachment_type.PNG,
            )

    def test_select_row(self, catalogue_page):
        """Проверяет возможность выбора строки из списка страницы-каталога"""
        with allure.step("Выбор строки admin"):
            catalogue_page.select_row("admin")

            allure.attach(
                catalogue_page.driver.get_screenshot_as_png(),
                name="Выбрана строка admin.",
                attachment_type=allure.attachment_type.PNG,
            )
    def test_info(self, catalogue_page):
        """Проверяет возможность получения подробной информации о программе"""
        catalogue_page.view_about()
        expected_texts = [
            "РЕД ВРМ",
            "1.0.0",
            "Лицензионное соглашение",
            "https://redos.red-soft.ru",
        ]
        page_text = catalogue_page.driver.page_source
        for text in expected_texts:
            assert text in page_text, f"Текст '{text}' не найден на странице"

    def test_logout(self, catalogue_page, login_page):
        """Проверяет возможность выхода из профиля"""
        catalogue_page.logout()
        login_submit = login_page.wait_for_element(login_page.SUBMIT_BUTTON)
        assert (
            login_submit.is_displayed()
        ), "Элемент подтверждения входа не отображается"
