from resources.main import MainResource


class LoginResource(MainResource):
    """Ресурсы авторизации"""

    # ДАННЫЕ АВТОРИЗАЦИИ АДМИНИСТРАТОРА
    ADMIN_AUTH_DATA = {"auth_strategy_id": "1", "name": "admin", "password": "admin"}

    # РЕСУРСЫ:
    USERS = MainResource.BASE_URL + "users/"
    ADMIN = MainResource.BASE_URL + "admin/"

    # РЕСУРСЫ USERS:
    AUTH = USERS + "auth"
    LOGIN = USERS + "login"
    REFRESH = USERS + "refresh"
    LOGOUT = USERS + "logout"
    STATUS = USERS + "status"

    # РЕСУРСЫ ADMIN:
    SEARCH_USER = ADMIN + "search_user"
    CHECK_CONNECTION = ADMIN + "check_connection"

    # def __init__(self):
    #     super().__init__()

    def get_auth_strategies(self):
        """Возвращает список стратегий авторизации"""
        return self.get(self.AUTH)

    def login_user(self, auth_data):
        """Производит авторизацию пользователя"""
        return self.session.post(self.LOGIN, data=auth_data)

    def login_admin(self):
        """Производит авторизацию администратора"""
        return self.login_user(self.ADMIN_AUTH_DATA)

    def logout_user(self):
        """Выход пользователя из системы"""
        return self.session.post(self.LOGOUT, json="")
