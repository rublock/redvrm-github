import pytest
import allure
import pages.config_redvrm as config_redvrm


@pytest.mark.usefixtures("login_admin")
class TestAuthenticators:
    """Тесты для страницы 'Аутентификаторы раздела 'Учётные записи''"""

    def test_create_authenticator(self, authenticators_page):
        """Проверяет возможность создания аутентификатора"""
        authenticators_page.open_page(
            authenticators_page.PAGES["authenticators"])
        with allure.step("Создание аутентификатора."):
            authenticators_page.create_authenticator(
                name="test_auth",
                description="Создаётся автотестом",
                auth_type="Внутренняя БД",
            )

            authenticators_page.select_row(row="test_auth")
            allure.attach(
                authenticators_page.driver.get_screenshot_as_png(),
                name="Аутентификатор создан.",
                attachment_type=allure.attachment_type.PNG,
            )
            authenticators_page.select_row(row="test_auth")

    def test_modify_authenticator(self, authenticators_page):
        """Проверяет возможность изменения аутентификатора"""
        authenticators_page.open_page(
            authenticators_page.PAGES["authenticators"])
        with allure.step("Создание аутентификатора."):
            authenticators_page.create_authenticator(
                name="auth_to_modify",
                description="Изменяется автотестом",
                auth_type="Внутренняя БД",
            )

            authenticators_page.select_row(row="auth_to_modify")
            allure.attach(
                authenticators_page.driver.get_screenshot_as_png(),
                name="Аутентификатор для изменения создан.",
                attachment_type=allure.attachment_type.PNG,
            )
            authenticators_page.select_row(row="auth_to_modify")

        with allure.step("Редактирование аутентификатора."):
            authenticators_page.modify_authenticator(
                authenticator="auth_to_modify", name="modified_auth"
            )

            authenticators_page.select_row(row="modified_auth")
            allure.attach(
                authenticators_page.driver.get_screenshot_as_png(),
                name="Аутентификатор изменён.",
                attachment_type=allure.attachment_type.PNG,
            )
            authenticators_page.select_row(row="modified_auth")

    def test_delete_authenticator(self, authenticators_page):
        """Проверяет возможность удаления аутентификатора"""
        authenticators_page.open_page(
            authenticators_page.PAGES["authenticators"])
        with allure.step("Создание аутентификатора."):
            authenticators_page.create_authenticator(
                name="auth_to_delete",
                description="Удаляется автотестом",
                auth_type="Внутренняя БД",
            )

            authenticators_page.select_row(row="auth_to_delete")
            allure.attach(
                authenticators_page.driver.get_screenshot_as_png(),
                name="Аутентификатор для удаления создан.",
                attachment_type=allure.attachment_type.PNG,
            )
            authenticators_page.select_row(row="auth_to_delete")

        with allure.step("Удаление аутентификатора."):
            # Тест не проходит из-за бага при удалении аутентификатора,
            # всплывает уведомление "пользователь успешно удален"
            authenticators_page.delete_authenticator(
                authenticator="auth_to_delete")

            allure.attach(
                authenticators_page.driver.get_screenshot_as_png(),
                name="Аутентификатор удалён.",
                attachment_type=allure.attachment_type.PNG,
            )

    def test_cancel_authenticator_deletion(self, authenticators_page):
        """Проверяет возможность отмены удаления аутентификатора"""
        authenticators_page.open_page(
            authenticators_page.PAGES["authenticators"])
        with allure.step("Создание аутентификатора."):
            authenticators_page.create_authenticator(
                name="auth_to_keep",
                description="Сохраняется автотестом при отмене удаления",
                auth_type="Внутренняя БД",
            )

            authenticators_page.select_row(row="auth_to_keep")
            allure.attach(
                authenticators_page.driver.get_screenshot_as_png(),
                name="Аутентификатор для удаления создан.",
                attachment_type=allure.attachment_type.PNG,
            )
            authenticators_page.select_row(row="auth_to_keep")

        with allure.step("Удаление аутентификатора."):
            authenticators_page.delete_authenticator(
                authenticator="auth_to_keep", cancel=True
            )

            authenticators_page.select_row(row="auth_to_keep")
            allure.attach(
                authenticators_page.driver.get_screenshot_as_png(),
                name="Аутентификатор сохранён.",
                attachment_type=allure.attachment_type.PNG,
            )
            authenticators_page.select_row(row="auth_to_keep")

    def test_success_authenticator_connection(self, authenticators_page):
        """Проверяет возможность проверки соединения аутентификатора"""
        authenticators_page.open_page(
            authenticators_page.PAGES["authenticators"])
        auth_settings = config_redvrm.AUTH_RA

        with allure.step("Создание аутентификатора."):
            authenticators_page.create_authenticator(
                name="auth_to_check",
                description="Должен пройти проверку соединения",
                auth_type="РЕД АДМ",
                auth_settings=auth_settings,
            )

            authenticators_page.select_row(row="auth_to_check")
            allure.attach(
                authenticators_page.driver.get_screenshot_as_png(),
                name="Аутентификатор создан.",
                attachment_type=allure.attachment_type.PNG,
            )
            authenticators_page.select_row(row="auth_to_check")

        with allure.step("Проверка соединения."):
            authenticators_page.check_connection(authenticator="auth_to_check")

            allure.attach(
                authenticators_page.driver.get_screenshot_as_png(),
                name="Соединение проверено.",
                attachment_type=allure.attachment_type.PNG,
            )

    def test_failed_authenticator_connection(self, authenticators_page):
        """Проверяет возможность проверки соединения аутентификатора"""
        authenticators_page.open_page(
            authenticators_page.PAGES["authenticators"])
        auth_settings = {
            "host_ip": "0.0.0.0",
            "login": "wrong\\login",
            "password": "fake",
            "advanced_settings": None,
        }

        with allure.step("Создание аутентификатора."):
            authenticators_page.create_authenticator(
                name="false_auth",
                description="Должен провалить проверку соединения",
                auth_type="РЕД АДМ",
                auth_settings=auth_settings,
            )

            authenticators_page.select_row(row="false_auth")
            allure.attach(
                authenticators_page.driver.get_screenshot_as_png(),
                name="Аутентификатор создан.",
                attachment_type=allure.attachment_type.PNG,
            )
            authenticators_page.select_row(row="false_auth")

        with allure.step("Проверка соединения."):
            authenticators_page.check_connection(
                authenticator="false_auth", connection="failed")

            allure.attach(
                authenticators_page.driver.get_screenshot_as_png(),
                name="Соединение проверено.",
                attachment_type=allure.attachment_type.PNG,
            )
