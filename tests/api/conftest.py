import pytest
from resources.login import LoginResource


@pytest.fixture
def login_resource():
    """Создаёт экземпляр ресурса авторизации"""
    # return LoginResource()
    lr = LoginResource()
    yield lr


@pytest.fixture
def authorize(login_resource):
    login_resource.login_admin()
