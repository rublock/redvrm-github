

import pytest
import allure


@pytest.mark.usefixtures("login_admin")
class TestUsers:
    """Тесты для страницы 'Пользователи' раздела 'Учётные записи'"""

    USERNAMES_LIST = [
        "john_doe", "alice123", "bob_smith", "emma.watson",
        "a", "username_with_underscores_and_numbers_123",
        "User.Name-With-Hyphen", "123456789", "___test___",
        "测试用户", "ユーザー名", "ім'я_користувача",
        " admin ", "null", "SELECT * FROM users",
        "<script>alert('xss')</script>",
        "very_long_username_that_exceeds_database_limit_12345678901234567890",
        "", "user@domain.com", "user+tag@gmail.com"
    ] # TODO: положить в config?

    @pytest.mark.parametrize("name", USERNAMES_LIST)
    def test_create_user(self, users_page, name):
        """Проверяет возможность создания пользователя"""
        users_page.open_page(users_page.PAGES["users"])
        with allure.step("Создание нового пользователя."):
            users_page.create_user(
                authenticator="DataBase",
                name=name,
                password="password",
                show_password=True,
            )

            # users_page.select_row("test_user") TODO: не проходит
            allure.attach(
                users_page.driver.get_screenshot_as_png(),
                name="Новый пользователь создан.",
                attachment_type=allure.attachment_type.PNG,
            )
            # users_page.select_row("test_user") TODO: не проходит

    def test_modify_user(self, users_page):
        """Проверяет возможность редактирования пользователя"""
        users_page.open_page(users_page.PAGES["users"])
        with allure.step("Создание пользователя для изменения."):
            users_page.create_user(
                authenticator="DataBase",
                name="user_to_modify",
                password="password",
                show_password=True,
            )
            users_page.select_row("user_to_modify")
            allure.attach(
                users_page.driver.get_screenshot_as_png(),
                name="Пользователь для изменения создан.",
                attachment_type=allure.attachment_type.PNG,
            )
            users_page.select_row("user_to_modify")

        with allure.step("Редактирование пользователя."):
            users_page.modify_user(user="user_to_modify", name="modified_user")
            users_page.select_row("modified_user")
            allure.attach(
                users_page.driver.get_screenshot_as_png(),
                name="Пользователь изменён.",
                attachment_type=allure.attachment_type.PNG,
            )

    def test_delete_user(self, users_page):
        """Проверяет возможность удаления пользователя"""
        users_page.open_page(users_page.PAGES["users"])
        with allure.step("Создание пользователя."):
            users_page.create_user(
                authenticator="DataBase",
                name="user_to_delete",
                password="password",
                show_password=True,
            )
            users_page.select_row("user_to_delete")
            allure.attach(
                users_page.driver.get_screenshot_as_png(),
                name="Пользователь для удаления создан.",
                attachment_type=allure.attachment_type.PNG,
            )
            users_page.select_row("user_to_delete")

        with allure.step("Удаление пользователя."):
            users_page.delete_user(user="user_to_delete")

            allure.attach(
                users_page.driver.get_screenshot_as_png(),
                name="Пользователь удалён.",
                attachment_type=allure.attachment_type.PNG,
            )

    def test_cancel_user_deletion(self, users_page):
        """Проверяет возможность удаления пользователя"""
        users_page.open_page(users_page.PAGES["users"])
        with allure.step("Создание пользователя."):
            users_page.create_user(
                authenticator="DataBase",
                name="user_to_keep",
                password="password",
                show_password=True,
            )
            users_page.select_row("user_to_keep")
            allure.attach(
                users_page.driver.get_screenshot_as_png(),
                name="Пользователь для удаления создан.",
                attachment_type=allure.attachment_type.PNG,
            )
            users_page.select_row("user_to_keep")

        with allure.step("Удаление пользователя."):
            users_page.delete_user(user="user_to_keep", cancel=True)
            users_page.select_row("user_to_keep")
            allure.attach(
                users_page.driver.get_screenshot_as_png(),
                name="Пользователь удалён.",
                attachment_type=allure.attachment_type.PNG,
            )
            users_page.select_row("user_to_keep")


    def test_double_name_user(self, users_page):
        users_page.open_page("Пользователи")
        users_page.create_user(
                authenticator="DataBase", name="user_name", password="password"
            )
        users_page.create_user(
                authenticator="DataBase", name="user_name", password="password", error_name="duplicate"
             )

    #Должен падать!!!! ТК баг не пофиксили
    def test_empty_password_user(self, users_page):
        users_page.open_page("Пользователи")
        users_page.create_user(
                authenticator="DataBase", name="empty_pass_user", password="", error_name="validation"
            )

