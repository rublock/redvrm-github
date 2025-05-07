import requests as r
import json as js


class MainResource:
    """Базовый класс для всех ресурсов"""

    BASE_URL = "http://10.81.112.164:8001/"

    def __init__(self):
        self.session = r.Session()

    def get(self, url, params=None):
        """
        Метод GET.

        :param url: URL-адрес для запроса.
        :param params: Параметры запроса.

        :returns: `<Response>` - ответ на запрос.
        """
        return r.get(url=url, params=params)

    def post(self, url, data=None, json=None, **kwargs):
        """
        Метод POST.

        :param url: URL-адрес для запроса.
        :param data: Данные тела запроса.
        :param json: JSON файл для тела запроса.
        :param **kwargs: Именные параметры запроса.

        :returns: `<Response>` - ответ на запрос.
        """
        return r.post(url=url, data=data, json=json, **kwargs)

    def put(self, url, data=None, json=None, **kwargs):
        """
        Метод PUT.
        
        :param url: URL-адрес для запроса.
        :param data: Данные тела запроса.
        :param json: JSON файл для тела запроса.
        :param **kwargs: Именные параметры запроса.

        :returns: `<Response>` - ответ на запрос.
        """
        return r.put(url=url, data=data, json=json, **kwargs)

    def delete(self, url, **kwargs):
        """
        Метод DELETE.

        :param url: URL-адрес для запроса.
        :param **kwargs: Именные параметры запроса.

        :returns: `<Response>` - ответ на запрос.
        """
        return r.delete(url=url, **kwargs)

    def head(self, url, **kwargs):
        """
        Метод HEAD.

        :param url: URL-адрес для запроса.
        :param **kwargs: Именные параметры запроса.

        :returns: `<Response>` - ответ на запрос.
        """
        return r.head(url=url, **kwargs)

    def options(self, url, **kwargs):
        """
        Метод OPTIONS.

        :param url: URL-адрес для запроса.
        :param **kwargs: Именные параметры запроса.

        :returns: `<Response>` - ответ на запрос.
        """
        return r.options(url=url, **kwargs)

    def as_json(self, response):
        """Возвращает результат запроса как JSON"""
        return js.loads(response.text)

    def as_list(self, response):
        """Возвращает результат запроса как список"""
        return list(self.as_json(response))
