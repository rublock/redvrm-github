from selenium.webdriver.common.by import By
import catalog_page as cp


class AgentsPage(cp.CatalogPage):
    """Страница 'Агенты' раздела 'Ресурсы'"""

    # ЛОКАТОРЫ ПУНКТОВ МЕНЮ:
    CHECK_CONNECTION = (By.XPATH, '//button[text()="Проверить соединение"]')

    # ЛОКАТОРЫ ФОРМЫ СОЗДАНИЯ АГЕНТА:
    IP_ADDRESS = (By.XPATH, '//input[@name="ip_addr"]')
    PORT = (By.XPATH, '//input[@name="port"]')

    def create_agent(self, ip_addr, port):
        """
        Создаёт новый агент с переданными параметрами

        :param ip_addr: IP адрес агента.
        :param port: Порт агента.
        """
        # Нажать кнопку "Создать"
        self.click_create_button()
        # Заполнение полей аутентификатора
        self._enter_ip(ip_addr)
        self._enter_port(port)
        # Подтверждение создания агента
        self.click_form_submit()
        # Проверка нотификации
        self.check_notification("агент успешно создан")

    def modify_agent(self, agent, ip_addr=None, port=None):
        """
        Изменяет параметры существующего агента.

        :param agent: IP адрес существующего агента.
        :param ip_addr: Новый ip адрес.
        :param  port: Новый порт.
        """
        # Выбор аутентификатора для изменения
        self.select_row(agent)
        # Нажать кнопку "Изменить"
        self.click_edit_button()
        # Изменение параметров аутентификатора
        if ip_addr:
            self._enter_ip(ip_addr)
        if port:
            self._enter_port(port)
        # Подтверждение изменения
        self.click_form_submit()
        # Проверка нотификации
        self.check_notification("агент успешно изменён")

    def delete_agent(self, ip_addr, cancel=False):
        """
        Удаляет агент по переданному IP адресу.

        :param ip_addr: Ip_addr существующего агента.
        :param cancel: Флаг отмены удаления, по умолчанию - не отменять.
        """
        # Выбрать аутентификатор для удаления
        self.select_row(row=ip_addr)
        # Нажать кнопку "Удалить"
        self.click_delete_button()
        if cancel:
            # Отмена удаления
            self.click_cancel_delete()
        else:
            # Подтверждение удаления
            self.click_confirm_delete()
            # Проверка нотификации
            self.check_notification("агент успешно удалён")

    def _enter_ip(self, ip_addr):
        """
        Вводит IP адрес агента в поле ввода.
        :param ip_addr: Ip_addr агента.
        """
        self.input_text(*self.IP_ADDRESS, text=ip_addr)

    def _enter_port(self, port):
        """
        Вводит порт агента.
        :param port: Порт.
        """
        self.input_text(*self.PORT, text=port, clear=True)

    def _click_check_connection_button(self):
        """Инициирует проверку соединения"""
        self.click_element(self.CHECK_CONNECTION)
