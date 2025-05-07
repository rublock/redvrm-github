from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import pages.config_redvrm as config_redvrm


class BasePage:
    """
    Базовый класс для веб-страниц.
    Обеспечивает общие методы для взаимодействия с элементами
    """

    # АДРЕС БРОКЕРА
    #BASE_URL = "http://10.81.112.185/"
    BASE_URL = config_redvrm.BASE_URL

    # ЛОКАТОР УВЕДОМЛЕНИЙ
    NOTIFICATION = (By.CSS_SELECTOR, "div#notistack-snackbar:last-child")

    def __init__(self, driver):
        """
        Инициализирует объект BasePage под управлением WebDriver.
        :param driver: Если True, запускает браузер в headless-режиме.
        """
        # Настройка времени ожидания
        self.default_wait_time = 30
        # Настройка драйвера
        self.driver = driver
        self.driver.implicitly_wait = self.default_wait_time
        self.driver.set_page_load_timeout(self.default_wait_time * 1.5)
        self.driver.get(self.BASE_URL)
        # Настройка действий
        self.actions = ActionChains(self.driver)

    def find_element(self, *locator):
        """
        Находит элемент на странице по указанному локатору.
        :param locator: Локатор элемента (например, XPath, CSS селектор).
        :return: Найденный элемент.
        """
        return self.driver.find_element(*locator)

    def find_elements(self, *locator):
        """
        Находит несколько элементов на странице по указанному локатору.
        :param locator: Локатор элементов (например, XPath, CSS селектор).
        :return: Список найденных элементов.
        """
        return self.driver.find_elements(*locator)

    def wait_for_element(self, locator, condition="presence", timeout=None):
        """
        Ожидает появления элемента на странице.

        :param locator: Локатор элемента (например, XPath, CSS селектор).
        :param condition: Стратегия ожидания, по умолчанию - появления элемента на странице.
        :param timeout: Время ожидания в секундах. Если не указано, используется значение по умолчанию.
        :return: Найденный элемент.
        """
        conditions = {
            "presence": EC.presence_of_element_located,
            "visible": EC.visibility_of_element_located,
            "clickable": EC.element_to_be_clickable,
            "invisible": EC.invisibility_of_element,
        }

        if isinstance(condition, str):
            condition = conditions.get(condition, EC.presence_of_element_located)

        if timeout is None:
            timeout = self.default_wait_time

        wait = WebDriverWait(self.driver, timeout)
        return wait.until(condition(locator))

    def scroll_to_element(self, locator):
        """
        Пролистывает страницу до элемента.
        :param locator: Локатора элемента.
        """
        element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def click_element(self, *locator, timeout=None, js_click=False, scroll=False):
        """
        Кликает на элемент на странице.
        :param locator: Локатор элемента (например, XPath, CSS селектор).
        :param timeout: Время ожидания в секундах. Если не указано, используется значение по умолчанию.
        :param js_click: Если True, используется JavaScript для клика.
        :param scroll: Если True, элемент прокручивается в видимую область перед кликом.
        """
        element = self.wait_for_element(
            *locator, timeout=timeout, condition="clickable"
        )
        if js_click:
            self.driver.execute_script("arguments[0].click();", element)
        else:
            if scroll:
                self.scroll_to_element(locator)
            element.click()

    def click_elements(self, *locator, index=None):
        """
        Кликает на элемент из списка элементов на странице.
        :param locator: Локатор элементов (например, XPath, CSS селектор).
        :param index: Индекс элемента, на который нужно кликнуть. Если не указан, кликает на первый элемент.
        """
        elements = self.find_elements(*locator)
        if index is not None:
            elements[index].click()
        else:
            elements[0].click()

    def input_text(
        self, *locator, text, clear=True, send_keys=True, click=False, timeout=None
    ):
        """
        Вводит текст в элемент на странице.

        :param locator: Локатор элемента (например, XPath, CSS селектор).
        :param text: Текст для ввода.
        :param clear: Если True, очищает текстовое поле перед вводом.
        :param send_keys: Если True, отправляет текст в поле.
        :param click: Если True, кликает на элемент перед вводом текста.
        :param timeout: Время ожидания в секундах. Если не указано, используется значение по умолчанию.
        """
        element = self.wait_for_element(locator, condition="visible", timeout=timeout)
        if click:
            element.click()
        if clear:
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.DELETE)
            self.actions.key_down(Keys.SHIFT).key_down(Keys.ALT).click(element).key_up(
                Keys.ALT
            ).key_up(Keys.SHIFT).perform()
        if send_keys:
            element.send_keys(text)

    def select_dropdown_by_visible_text(self, locator, text, timeout=None):
        """
        Выбирает элемент из выпадающего списка по тексту.
        :param locator: Локатор элемента <li>.
        :param text: Текст, который нужно выбрать.
        :param timeout: Время ожидания в секундах. Если не указано, используется значение по умолчанию.
        """
        # Ждем, пока элементы не будут видны
        elements = self.wait_for_element(locator, condition="clickable", timeout=timeout)
        # Находим все элементы списка по локатору
        elements = self.find_elements(*locator)
        # Перебираем элементы и кликаем по нужному тексту
        for element in elements:
            if element.text == text:
                element.click()
                break
        else:
            raise ValueError(f"Не найден элемент с текстом: {text}")

    def get_text(self, *locator):
        """
        Извлекает текст с элемента на странице.
        :param locator: Локатор элемента.
        """
        element = self.wait_for_element(locator, condition="visible", timeout=None)
        return element.text

    def press_enter(self):
        """Отправляет клавишу Enter"""
        self.actions.send_keys(Keys.ENTER).perform()

    def press_escape(self):
        """Отправляет клавишу Escape"""
        self.actions.send_keys(Keys.ESCAPE).perform()

    def assert_current_url(self, expected_url, timeout=None):
        """
        Проверяет, что текущий URL соответствует ожидаемому.
        :param expected_url: Ожидаемый URL.
        :param timeout: Максимальное время ожидания (в секундах).
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_to_be(expected_url))
        except Exception as e:
            raise AssertionError(
                f"Ожидался URL: {expected_url}, но был получен: {self.driver.current_url}. "
                f"Превышено время ожидания {timeout} секунд."
            )

    def format_xpath(self, locator, data):
        """
        Подставляет переданные данные в локатор для форматирования.
        :param locator: Локатор элемента для форматирования.
        :param data: Данные для подстановки.
        """
        by, xpath = locator
        xpath = xpath.format(data)
        return by, xpath

    def set_checkbox(self, locator, state=True):
        """
        Переключает чекбокс в переданное состояние

        :param locator: Локатор элемента span
        """
        element = self.wait_for_element(locator, condition="visible")
        element_classes = element.get_attribute("class")
        if "Mui-checked" not in element_classes and state:
            self.click_element(locator)
        if "Mui-checked" in element_classes and not state:
            self.click_element(locator)

    def check_notification(self, expected_message):
        """
        Проверяет всплывающее окно с оповещением о действии.
        :param expected_message: Ожидаемое оповещение.
        """
        element = self.wait_for_element(self.NOTIFICATION, condition="visible")
        assert element.text == expected_message
        self.wait_for_element(self.NOTIFICATION, condition="invisible")

    def check_result(self, locator, data, error_message):
        """
        Проверяет действительно ли добавлен элемент
        :param locator: Локатор элемента
        :param data: Данные для проверки
        :param error_message: Сообщение об ошибке
        """
        if '{}' in locator[1]:
            locator = self.format_xpath(locator, data)
        element = self.wait_for_element(locator)
        assert data == element.text, error_message
