import pytest
import allure


@pytest.mark.usefixtures("login_admin")
class TestGroups:
    """Тесты для страницы 'Группы' раздела 'Учётные записи'"""

    def test_create_group(self, groups_page):
        """Проверяет возможность создания группы"""
        groups_page.open_page(groups_page.PAGES["groups"])
        with allure.step("Создание группы."):
            groups_page.create_group(name="test_group")

            allure.attach(
                groups_page.driver.get_screenshot_as_png(),
                name="Группа создана.",
                attachment_type=allure.attachment_type.PNG,
            )

    def test_modify_group(self, groups_page):
        """Проверяет возможность изменения группы"""
        groups_page.open_page(groups_page.PAGES["groups"])
        with allure.step("Создание группы."):
            groups_page.create_group(name="group_to_modify")

            allure.attach(
                groups_page.driver.get_screenshot_as_png(),
                name="Группа для изменения создана.",
                attachment_type=allure.attachment_type.PNG,
            )

        with allure.step("Редактирование группы."):
            groups_page.modify_group(
                group="group_to_modify",
                name="modified_group",
            )

            allure.attach(
                groups_page.driver.get_screenshot_as_png(),
                name="Группа изменена.",
                attachment_type=allure.attachment_type.PNG,
            )

    def test_delete_group(self, groups_page):
        """Проверяет возможность удаления группы"""
        groups_page.open_page(groups_page.PAGES["groups"])
        with allure.step("Создание группы."):
            groups_page.create_group(name="group_to_delete")

            allure.attach(
                groups_page.driver.get_screenshot_as_png(),
                name="Группа для удаления создана.",
                attachment_type=allure.attachment_type.PNG,
            )

        with allure.step("Удаление Группы."):
            groups_page.delete_group(group="group_to_delete")

            allure.attach(
                groups_page.driver.get_screenshot_as_png(),
                name="Группа удалена.",
                attachment_type=allure.attachment_type.PNG,
            )

    def test_cancel_group_deletion(self, groups_page):
        """Проверяет возможность удаления группы"""
        groups_page.open_page(groups_page.PAGES["groups"])
        with allure.step("Создание группы."):
            groups_page.create_group(name="group_to_keep")

            allure.attach(
                groups_page.driver.get_screenshot_as_png(),
                name="Группа для сохранения создана.",
                attachment_type=allure.attachment_type.PNG,
            )

        with allure.step("Сохранение группы."):
            groups_page.delete_group(group="group_to_keep", cancel=True)

            allure.attach(
                groups_page.driver.get_screenshot_as_png(),
                name="Группа сохранена.",
                attachment_type=allure.attachment_type.PNG,
            )

    def test_add_user_to_group(self, users_page, groups_page):
        """Проверяет возможность добавления пользователя в группу доступа"""
        # Создание пользователя для добавления
        users_page.open_page(users_page.PAGES["users"])
        users_page.create_user(authenticator="DataBase", name="user", password="user")
        # Добавление пользователя в группу
        groups_page.open_page(groups_page.PAGES["groups"])
        groups_page.create_group(name="group_to_add_user")
        groups_page.add_user(group="group_to_add_user", user="user")
