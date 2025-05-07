import pytest
import allure
import pages.config_redvrm as config_redvrm


@pytest.mark.usefixtures("login_admin")
class TestProviders:
    """Тесты для страницы 'Поставщики' раздела 'Ресурсы'"""

    PROVIDER = config_redvrm.PROVIDER

    def test_create_provider(self, providers_page):
        """Проверяет возможность создания поставщика"""
        providers_page.open_page(providers_page.PAGES["providers"])
        with allure.step("Создание нового поставщика."):
            providers_page.create_provider(
                name="test_provider",
                host_ip=self.PROVIDER["host_ip"],
                login=self.PROVIDER["login"],
                password=self.PROVIDER["login"],
            )

            providers_page.select_row("test_provider")
            allure.attach(
                providers_page.driver.get_screenshot_as_png(),
                name="Новый поставщик создан.",
                attachment_type=allure.attachment_type.PNG,
            )
            providers_page.select_row("test_provider")

    def test_modify_provider(self, providers_page):
        """Проверяет возможность редактирования поставщика"""
        providers_page.open_page(providers_page.PAGES["providers"])
        with allure.step("Создание нового поставщика."):
            providers_page.create_provider(
                name="provider_to_modify",
                host_ip=self.PROVIDER["host_ip"],
                login=self.PROVIDER["login"],
                password=self.PROVIDER["password"],
            )

            providers_page.select_row("provider_to_modify")
            allure.attach(
                providers_page.driver.get_screenshot_as_png(),
                name="Новый поставщик создан.",
                attachment_type=allure.attachment_type.PNG,
            )
            providers_page.select_row("provider_to_modify")

        with allure.step("Редактирование поставщика."):
            providers_page.modify_provider(
                provider="provider_to_modify",
                name="modified_provider"
            )

            providers_page.select_row("modified_provider")
            allure.attach(
                providers_page.driver.get_screenshot_as_png(),
                name="Поставщик отредактирован.",
                attachment_type=allure.attachment_type.PNG,
            )
            providers_page.select_row("modified_provider")

    def test_delete_provider(self, providers_page):
        """Проверяет возможность удаления поставщика"""
        providers_page.open_page(providers_page.PAGES["providers"])
        with allure.step("Создание нового поставщика."):
            providers_page.create_provider(
                name="provider_to_delete",
                host_ip=self.PROVIDER["host_ip"],
                login=self.PROVIDER["login"],
                password=self.PROVIDER["password"],
            )

            providers_page.select_row("provider_to_delete")
            allure.attach(
                providers_page.driver.get_screenshot_as_png(),
                name="Новый поставщик создан.",
                attachment_type=allure.attachment_type.PNG,
            )
            providers_page.select_row("provider_to_delete")

        with allure.step("Удаление поставщика."):
            providers_page.delete_provider(provider="provider_to_delete")

            allure.attach(
                providers_page.driver.get_screenshot_as_png(),
                name="Поставщик удалён.",
                attachment_type=allure.attachment_type.PNG,
            )

    def test_cancel_provider_deletion(self, providers_page):
        """Проверяет возможность отмены удаления поставщика"""
        providers_page.open_page(providers_page.PAGES["providers"])
        with allure.step("Создание нового поставщика."):
            providers_page.create_provider(
                name="provider_to_keep",
                host_ip=self.PROVIDER["host_ip"],
                login=self.PROVIDER["login"],
                password=self.PROVIDER["password"],
            )

            providers_page.select_row("provider_to_keep")
            allure.attach(
                providers_page.driver.get_screenshot_as_png(),
                name="Новый поставщик создан.",
                attachment_type=allure.attachment_type.PNG,
            )
            providers_page.select_row("provider_to_keep")

        with allure.step("Отмена удаления поставщика."):
            providers_page.delete_provider(
                provider="provider_to_keep", cancel=True)

            providers_page.select_row("provider_to_keep")
            allure.attach(
                providers_page.driver.get_screenshot_as_png(),
                name="Поставщик отредактирован.",
                attachment_type=allure.attachment_type.PNG,
            )
            providers_page.select_row("provider_to_keep")

    def test_succes_provider_connection(self, providers_page):
        """Проверяет успешное подключение поставщика"""
        providers_page.open_page(providers_page.PAGES["providers"])
        with allure.step("Создание нового поставщика."):
            providers_page.create_provider(
                name="provider_to_check",
                host_ip=self.PROVIDER["host_ip"],
                login=self.PROVIDER["login"],
                password=self.PROVIDER["password"],
            )

            providers_page.select_row("provider_to_check")
            allure.attach(
                providers_page.driver.get_screenshot_as_png(),
                name="Новый поставщик создан.",
                attachment_type=allure.attachment_type.PNG,
            )
            providers_page.select_row("provider_to_check")

        with allure.step("Проверка соединения."):
            providers_page.check_connection("provider_to_check")

            allure.attach(
                providers_page.driver.get_screenshot_as_png(),
                name="Соединение проверено.",
                attachment_type=allure.attachment_type.PNG,
            )

    def test_failed_provider_connection(self, providers_page):
        """Проверяет неудачное подключение поставщика"""
        providers_page.open_page(providers_page.PAGES["providers"])
        with allure.step("Создание нового поставщика."):
            providers_page.create_provider(
                name="false_provider",
                host_ip="0.0.0.0",
                login="wrong@credentials",
                password="fake",
            )

            providers_page.select_row("false_provider")
            allure.attach(
                providers_page.driver.get_screenshot_as_png(),
                name="Новый поставщик создан.",
                attachment_type=allure.attachment_type.PNG,
            )
            providers_page.select_row("false_provider")

        with allure.step("Проверка соединения."):
            providers_page.check_connection(
                "false_provider", connection="failed")

            allure.attach(
                providers_page.driver.get_screenshot_as_png(),
                name="Соединение проверено.",
                attachment_type=allure.attachment_type.PNG,
            )
