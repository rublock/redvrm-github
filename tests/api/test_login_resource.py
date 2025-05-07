import allure
import pytest


@pytest.fixture
def auth_data():
    return {"auth_strategy_id": "1", "name": "admin", "password": "admin"}


class TestLogin:
    """API-тесты для ресурса авторизации"""

    def test_get_first_auth_strategy(self, login_resource):
        """Проверяет возможность получения первой стратегии авторизации (DataBase)"""
        response = login_resource.get_auth_strategies()
        assert response.status_code == 200

        auth_strats = login_resource.as_list(response)
        data_base = auth_strats[0]

        assert data_base["id"] == 1
        assert data_base["auth_name"] == "DataBase"

    def test_login_user(self, login_resource, auth_data):
        """Проверет возможность авторизации пользователя"""
        with allure.step("Проверка на наличие стратегии авторизации в системе"):
            response = login_resource.get_auth_strategies()
            assert response.status_code == 200

            auth_strats = login_resource.as_list(response)
            data_base = auth_strats[0]
            assert int(auth_data["auth_strategy_id"]) == data_base["id"]

        with allure.step("Проверка успешной авторизации"):
            response = login_resource.login_user(auth_data)
            assert response.status_code == 200

            body = login_resource.as_json(response)
            assert body["message"] == "Login successful"

    # @pytest.mark.usefixtures("authorize")
    def test_logout_user(self, login_resource, auth_data):
        """Проверяет возможность выхода пользователя"""

        with allure.step("Проверка на наличие стратегии авторизации в системе"):
            response = login_resource.get_auth_strategies()
            assert response.status_code == 200

            data_base = login_resource.as_list(response)[0]
            assert int(auth_data["auth_strategy_id"]) == data_base["id"]

        with allure.step("Проверка успешной авторизации"):
            response = login_resource.login_user(auth_data)
            assert response.status_code == 200

            body = login_resource.as_json(response)
            assert body["message"] == "Login successful"

        with allure.step("Проверка выхода"):
            response = login_resource.logout_user()
            assert response.status_code == 200

            body = login_resource.as_json(response)
            assert body["message"] == "Logged out user successfully"
