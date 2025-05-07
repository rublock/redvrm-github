import allure


class TestAuthorization:
    """Тесты для страницы авторизации"""

    def test_successful_login_as_admin(self, login_page):
        """Проверка успешной авторизации администратора"""
        with allure.step("Авторизация администратора"):
            login_page.login_admin(authenticator="DataBase")

            allure.attach(
                login_page.driver.get_screenshot_as_png(),
                name="Успешная авторизация.",
                attachment_type=allure.attachment_type.PNG,
            )

    def test_successful_login_as_user(self, login_page, users_page, catalogue_page):
        """Проверка успешной авторизации пользователя"""
        login_page.login_admin(authenticator="DataBase")
        users_page.open_page(users_page.PAGES["users"])
        users_page.create_user(
            authenticator="DataBase",
            name="user_successful_login",
            password="user",
            show_password=True,
        )
        catalogue_page.logout()
        with allure.step("Авторизация пользователя"):
            login_page.login_user(
                authenticator="DataBase", username="user_successful_login", password="user"
            )

        allure.attach(
            login_page.driver.get_screenshot_as_png(),
            name="Успешная авторизация.",
            attachment_type=allure.attachment_type.PNG,
        )

    def test_unsuccessful_login_as_user(self, login_page):
        """Проверка успешной авторизации пользователя"""
        login_page.login_user(
                authenticator="DataBase", username="no_user", password="no_user", error_name="validation"
        )