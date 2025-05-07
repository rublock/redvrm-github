import pytest
import allure
import pages.config_redvrm as config_redvrm


@pytest.mark.usefixtures("login_admin")
class TestPermissions:
    """Тесты для страницы 'Разрешения' раздела 'Настройки'"""

    settings = config_redvrm.PERMISSION

    def test_create_permission(self, permissions_page):
        """Проверяет возможность создания разрешения"""
        permissions_page.open_page(permissions_page.PAGES["permissions"])
        with allure.step("Создание разрешения"):
            permissions_page.create_permission(
                name="test_permission", settings=self.settings
            )
            permissions_page.select_row("test_permission")
            allure.attach(
                permissions_page.driver.get_screenshot_as_png(),
                name="Новое разрешение создано.",
                attachment_type=allure.attachment_type.PNG,
            )
            permissions_page.select_row("test_permission")

    def test_modify_permsiion(self, permissions_page):
        """Проверяет возможность создания разрешения"""
        permissions_page.open_page(permissions_page.PAGES["permissions"])
        with allure.step("Создание разрешения"):
            permissions_page.create_permission(
                name="permission_to_modify", settings=self.settings
            )
            permissions_page.select_row("permission_to_modify")
            allure.attach(
                permissions_page.driver.get_screenshot_as_png(),
                name="Разрешение для редактирования создано.",
                attachment_type=allure.attachment_type.PNG,
            )
            permissions_page.select_row("permission_to_modify")

        with allure.step("Изменение разрешения"):
            permissions_page.modify_permission(
                permission="permission_to_modify", name="modified_permission"
            )
            permissions_page.select_row("modified_permission")
            allure.attach(
                permissions_page.driver.get_screenshot_as_png(),
                name="Разрешение изменено.",
                attachment_type=allure.attachment_type.PNG,
            )
            permissions_page.select_row("modified_permission")

    def test_delete_permssion(self, permissions_page):
        """Проверяет возможность создания разрешения"""
        permissions_page.open_page(permissions_page.PAGES["permissions"])
        with allure.step("Создание разрешения"):
            permissions_page.create_permission(
                name="permission_to_delete", settings=self.settings
            )
            permissions_page.select_row("permission_to_delete")
            allure.attach(
                permissions_page.driver.get_screenshot_as_png(),
                name="Разрешение для удаления создано.",
                attachment_type=allure.attachment_type.PNG,
            )
            permissions_page.select_row("permission_to_delete")

        with allure.step("Удаление разрешения"):
            permissions_page.delete_permission(permission="permission_to_delete")
            allure.attach(
                permissions_page.driver.get_screenshot_as_png(),
                name="Разрешение удалено.",
                attachment_type=allure.attachment_type.PNG,
            )

    def test_cacel_permssion_deletion(self, permissions_page):
        """Проверяет возможность создания разрешения"""
        permissions_page.open_page(permissions_page.PAGES["permissions"])
        with allure.step("Создание разрешения"):
            permissions_page.create_permission(
                name="permission_to_keep", settings=self.settings
            )
            permissions_page.select_row("permission_to_keep")
            allure.attach(
                permissions_page.driver.get_screenshot_as_png(),
                name="Разрешение для сохранения создано.",
                attachment_type=allure.attachment_type.PNG,
            )
            permissions_page.select_row("permission_to_keep")

        with allure.step("Отмена удаления разрешения"):
            permissions_page.delete_permission(
                permission="permission_to_keep", cancel=True
            )
            permissions_page.select_row("permission_to_keep")
            allure.attach(
                permissions_page.driver.get_screenshot_as_png(),
                name="Разрешение сохранено.",
                attachment_type=allure.attachment_type.PNG,
            )
            permissions_page.select_row("permission_to_keep")
