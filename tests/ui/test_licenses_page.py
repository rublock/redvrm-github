import allure
import pytest

import pages.config_redvrm as config_redvrm


@pytest.mark.usefixtures("login_admin")
class TestLicenses:
    """Тесты для страницы 'Лицензии' раздела 'Лицензирование'"""

    LICENSE = config_redvrm.LICENSE

    def choose_license(self, key):
        """Находит по ключу нужную лицензию из списка словарей"""
        return next(
            (item for item in self.LICENSE if item["key"] == key),
            None,
        )

    def test_create_license(self, licenses_page):
        """Проверяет возможность добавления лицензии"""
        licenses_page.open_page(licenses_page.PAGES["licenses"])
        with allure.step("Добавление лицензии"):
            license = self.choose_license("BBBD-BBBO-WDBB-BCBL-BBBN-BRJE")
            licenses_page.create_license(license["key"])
            licenses_page.select_license(license["key"])
            allure.attach(
                licenses_page.driver.get_screenshot_as_png(),
                name="Новая лицензия добавлена.",
                attachment_type=allure.attachment_type.PNG,
            )
            licenses_page.select_license(license["key"])

    def test_delete_license(self, licenses_page):
        """Проверяет возможность удаления лицензии"""
        licenses_page.open_page(licenses_page.PAGES["licenses"])
        with allure.step("Добавление лицензии"):
            license = self.choose_license("QDBB-BBBB-BBLL-BDBB-BBCE-BDWX")
            licenses_page.create_license(license["key"])
            licenses_page.select_license(license["key"])

            allure.attach(
                licenses_page.driver.get_screenshot_as_png(),
                name="Лицензия для удаления добавлена.",
                attachment_type=allure.attachment_type.PNG,
            )
            licenses_page.select_license(license["key"])

        with allure.step("Удаление лицензии"):
            licenses_page.delete_license(license["key"])

            allure.attach(
                licenses_page.driver.get_screenshot_as_png(),
                name="Лицензия удалена.",
                attachment_type=allure.attachment_type.PNG,
            )

    def test_cancel_license_deletion(self, licenses_page):
        """Проверяет возможность удаления лицензии"""
        licenses_page.open_page(licenses_page.PAGES["licenses"])
        with allure.step("Добавление лицензии"):
            license = self.choose_license("BCDB-BBLN-DEBQ-BBBD-BBBB-LSLM")
            licenses_page.create_license(license["key"])
            licenses_page.select_license(license["key"])
            allure.attach(
                licenses_page.driver.get_screenshot_as_png(),
                name="Лицензия для сохранения добавлена.",
                attachment_type=allure.attachment_type.PNG,
            )
            licenses_page.select_license(license["key"])

        with allure.step("Отмена удаления лицензии"):
            licenses_page.delete_license(license["key"], cancel=True)
            licenses_page.select_license(license["key"])
            allure.attach(
                licenses_page.driver.get_screenshot_as_png(),
                name="Лицензия сохранена.",
                attachment_type=allure.attachment_type.PNG,
            )
            licenses_page.select_license(license["key"])

    def test_activate_license(self, licenses_page):
        """Проверяет возможность активации лицензии по типу"""
        licenses_page.open_page(licenses_page.PAGES["licenses"])
        with allure.step("Добавление лицензии"):
            license = self.choose_license("BBBC-BRDN-EBDB-BBDL-BBBL-BWTM")
            licenses_page.create_license(license["key"])
            licenses_page.select_license(license["key"])
            allure.attach(
                licenses_page.driver.get_screenshot_as_png(),
                name="Лицензия для активации добавлена.",
                attachment_type=allure.attachment_type.PNG,
            )
            licenses_page.select_license(license["key"])

        with allure.step("Активация лицензии"):
            licenses_page.activate_license(
                license["redaction_type"],
                license["license_type"],
                license["license_subtype"],
            )

            licenses_page.select_license(license["key"])
            allure.attach(
                licenses_page.driver.get_screenshot_as_png(),
                name="Лицензия активирована.",
                attachment_type=allure.attachment_type.PNG,
            )
            licenses_page.select_license(license["key"])
