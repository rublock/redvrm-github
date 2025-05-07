import pytest
import pages.config_redvrm as config_redvrm

@pytest.mark.usefixtures("login_admin")
class TestAccessGroups:
    """Тесты для страницы 'Группы доступа' раздела 'Настройки'"""

    permission_flag = False

    @staticmethod
    def create_permission(permissions_page):
        """Создаёт разрешение, используемое в тестах"""
        permissions_page.open_page(permissions_page.PAGES["permissions"])
        permission_name = "test_permission"
        permission_settings = config_redvrm.PERMISSION
        permissions_page.create_permission(permission_name, permission_settings)

    def test_create_access_group(self, permissions_page, access_groups_page):
        """Проверяет возможность создания группы доступа"""
        if not self.permission_flag:
            self.create_permission(permissions_page)
            self.permission_flag = True
        access_groups_page.open_page(access_groups_page.PAGES["access_groups"])
        access_groups_page.create_access_group("test_access", "test_permission")

    def test_modify_access_group(self, permissions_page, access_groups_page):
        """Проверяет возможность изменения группы доступа"""
        if not self.permission_flag:
            self.create_permission(permissions_page)
            self.permission_flag = True
        access_groups_page.open_page(access_groups_page.PAGES["access_groups"])
        access_groups_page.create_access_group("access_to_modify", "test_permission")
        access_groups_page.modify_access_group("access_to_modify", "access_modified")

    def test_delete_access_group(self, permissions_page, access_groups_page):
        """Проверяет возможность удаления группы доступа"""
        if not self.permission_flag:
            self.create_permission(permissions_page)
            self.permission_flag = True

        access_groups_page.open_page(access_groups_page.PAGES["access_groups"])
        access_groups_page.create_access_group("access_to_delete", "test_permission")
        access_groups_page.delete_access_group("access_to_delete")

    def test_cancel_access_group_deletion(self, permissions_page, access_groups_page):
        """Проверяет возможность отмены удаления группы доступа"""
        if not self.permission_flag:
            self.create_permission(permissions_page)
            self.permission_flag = True

        access_groups_page.open_page(access_groups_page.PAGES["access_groups"])
        access_groups_page.create_access_group("access_to_keep", "test_permission")
        access_groups_page.delete_access_group("access_to_keep", cancel=True)

    def test_view_access_group_details(self, permissions_page, access_groups_page):
        """Проверяет возможность получения"""
        if not self.permission_flag:
            self.create_permission(permissions_page)
            self.permission_flag = True

        access_groups_page.open_page(access_groups_page.PAGES["access_groups"])
        access_groups_page.create_access_group("detailed_access", "test_permission")
        access_groups_page.view_details("detailed_access")

    def test_add_user_to_access_group(
        self, users_page, permissions_page, access_groups_page
    ):
        """Проверяет возможность добавления пользователя в группу доступа"""
        users_page.open_page(users_page.PAGES["users"])
        users_page.create_user(authenticator="DataBase", name="user", password="user")

        if not self.permission_flag:
            self.create_permission(permissions_page)
            self.permission_flag = True

        access_groups_page.open_page(access_groups_page.PAGES["access_groups"])
        access_groups_page.create_access_group("user_access", "test_permission")
        access_groups_page.view_details("user_access")
        access_groups_page.add_details_entry(user="user")

    def test_add_group_to_access_group(
        self, groups_page, permissions_page, access_groups_page
    ):
        """Проверяет возможность добавления группы в группу доступа"""
        groups_page.open_page(groups_page.PAGES["groups"])
        groups_page.create_group(name="test_group")

        if not self.permission_flag:
            self.create_permission(permissions_page)
            self.permission_flag = True

        access_groups_page.open_page(access_groups_page.PAGES["access_groups"])
        access_groups_page.create_access_group("group_access", "test_permission")
        access_groups_page.view_details("group_access")
        access_groups_page.add_details_entry(group="test_group")
