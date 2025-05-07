"""Файл конфигурации РЕД ВРМ"""

# ------------------------------------------
# АКТУАЛИЗИРУЕМЫЕ ДАННЫЕ
BASE_URL = "http://10.81.112.189/"  # АДРЕС БРОКЕРА. В Тустере отсутствует.
# АДРЕС БРОКЕРА, при необходимости, каждый корректирует на свой для локальных проверок.

# TODO: актуализировать параметры аутентификатора РЕД АДМ для успешного прохождения теста на подключение LDAP-аутентификатора.
AUTH_RA = {
    "host_ip": "10.81.108.237",
    "port": "636",
    "login": "redvrm\\administrator",
    "password": "qqqwww13!",
    "advanced_settings": {"use_ssl": True},
}

# TODO: актуализировать параметры поставщика для успешного прохождения тестов страницы поставщиков.
PROVIDER = {
    "host_ip": "10.81.108.113",
    "login": "admin@internal",
    "password": "qqqwww12!",
    "settings": {
        # В ссответсвующих проверках изменить по ключу:
        "timeout": "15",
        "use_ssl": True,
        "max_create_package": "5",
        "max_delete_package": "2",
    },
}

LICENSE = [
    {
        "key": "BBBD-BBBO-WDBB-BCBL-BBBN-BRJE",
        "license_type": "Именная",
        "license_subtype": "Коммерческая",
        "redaction_type": "Стандартная",
    },
    {
        "key": "QDBB-BBBB-BBLL-BDBB-BBCE-BDWX",
        "license_type": "Конкурентная",
        "license_subtype": "Коммерческая",
        "redaction_type": "Стандартная",
    },
    {
        "key": "BCDB-BBLN-DEBQ-BBBD-BBBB-LSLM",
        "license_type": "Конкурентная",
        "license_subtype": "Тестовая",
        "redaction_type": "Стандартная",
    },
    {
        "key": "BBBC-BRDN-EBDB-BBDL-BBBL-BWTM",
        "license_type": "Конкурентная",
        "license_subtype": "Учебная",
        "redaction_type": "Стандартная",
    },
]

# ПАРАМЕТРЫ РАЗРЕШЕНИЯ:
PERMISSION = {
    "fullscreen": False,
    "width": "800",
    "heigh": "600",
    "dynamic_resolution": False,
    # В соответствующих проверках изменить обращением по ключу:
    "clipboard": "False",
    "smart_card": False,
}
# ------------------------------------------

# ЗНАЧЕНИЯ АВТОРИЗАЦИИ ПО УМОЛЧАНИЮ
ADMINISTRATOR_USERNAME = "admin"
ADMINISTRATOR_PASSWORD = "admin"
DEFAULT_AUTHENTICATOR = "DataBase"

# РАЗДЕЛЫ МЕНЮ СИСТЕМЫ
SECTIONS = {
    "credentials": "Учётные записи",
    "resources": "Ресурсы",
    "licensing": "Лицензирование",
    "options": "Настройки",
}

# СТРАНИЦЫ МЕНЮ СИСТЕМЫ
PAGES = {
    "authenticators": "Аутентификаторы",
    "groups": "Группы",
    "users": "Пользователи",
    "agents": "Агенты",
    "pools": "Пулы",
    "providers": "Поставщики",
    "workspaces": "Рабочие места",
    "licenses": "Лицензии",
    "sessions": "Сессии",
    "permissions": "Разрешения",
    "access_groups": "Группы доступа",
    "user_page": "Страница пользователя",
}

# УВЕДОМЛЕНИЯ НА ВСПЛЫВАЮЩИХ ОКНАХ
NOTIFICATIONS = {
    # ДЛЯ СТРАНИЦЫ АВТОРИЗАЦИИ
    "login_success": "Авторизация прошла успешно",
    "login_failed": "Не удалось авторизоваться",

    # ДЛЯ СТРАНИЦЫ "АУТЕНТИФИКАТОРЫ" РАЗДЕЛА "УЧЁТНЫЕ ЗАПИСИ"
    "auth_create": "аутентификатор успешно создан",
    "auth_modify": "аутентификатор успешно изменён",
    "auth_delete": "аутентификатор успешно удалён",
    "auth_check_success": "аутентификатор успешно проверен",
    "auth_check_failed": "Не удалось установить соединение",

    # ДЛЯ СТРАНИЦЫ "ГРУППЫ" РАЗДЕЛА "УЧЁТНЫЕ ЗАПИСИ"
    "groups_create": "группа успешно создана",
    "groups_modify": "группа успешно изменена",
    "groups_delete": "группа успешно удалена",
    "groups_add_user": "пользователь успешно добавлен",
    "groups_delete_user": "пользователь успешно удалён",

    # ДЛЯ СТРАНИЦЫ "ПОЛЬЗОВАТЕЛИ" РАЗДЕЛА "УЧЁТНЫЕ ЗАПИСИ"
    "user_create": "пользователь успешно создан",
    "user_modify": "пользователь успешно изменён",
    "user_delete": "пользователь успешно удалён",
    "user_block": "пользователь успешно заблокирован",
    "user_unblock": "пользователь успешно разблокирован",
    "users_duplicate": ('Ошибка: {"non_field_errors":'
                        '["The fields name, auth_strategy must make a unique set."]}'),
    "users_ldap_missing": 'Ошибка: "User not found in LDAP"',
    "users_empty_password": "Заполните поле пароль",

    # ДЛЯ СТРАНИЦЫ "АГЕНТЫ" РАЗДЕЛА "РЕСУРСЫ"
    "agents_create": "агент успешно создан",
    "agents_modify": "агент успешно изменён",
    "agents_delete": "агент успешно удалён",
    "agents_check_success": "агент успешно проверен",
    "agents_check_failed": "агент не прошел проверку",
    "agents_duplicate": 'Ошибка: {"ip_addr":["agent with this ip addr already exists."]}',

    # ДЛЯ СТРАНИЦЫ "ПОСТАВЩИКИ" РАЗДЕЛА "РЕСУРСЫ"
    "providers_create": "поставщик успешно создан",
    "providers_modify": "поставщик успешно изменён",
    "providers_delete": "поставщик успешно удалён",
    "providers_check_success": "поставщик успешно проверен",
    "providers_check_failed": "Не удалось проверить соединение",

    # ДЛЯ СТРАНИЦЫ "ПУЛЫ" РАЗДЕЛА "РЕСУРСЫ"
    # TODO: актуализировать после исправления багов с уведомлениями
    # "pools_create": "пул успешно создан",
    "pools_modify": "пул успешно изменён",
    "pools_delete": "пул успешно удалён",
    "pools_agent_add": "агент успешно добавлен",
    # "pools_agent_delete": "агент успешно удалён",
    "pools_agent_on": "агент успешно включен",
    "pools_agent_off": "агент успешно выключен",
    "pools_agent_stop": "агент успешно приостановлен",
    "pools_agent_restart": "агент успешно перезагружен",

    # ДЛЯ СТРАНИЦЫ "РАБОЧИЕ МЕСТА"
    "workspaces_create": "рабочее место успешно создано",
    "workspaces_modify": "рабочее место успешно изменено",
    "workspaces_delete": "рабочее место успешно удалено",

    # ДЛЯ СТРАНИЦЫ "ЛИЦЕНЗИИ" РАЗДЕЛА "ЛИЦЕНЗИРОВАНИЕ"
    "licenses_create": "лицензия успешно создана",
    "licenses_delete": "лицензия успешно удалена",
    "licenses_activate": "Лицензии успешно активированы",
    "licenses_duplicate": ('Ошибка: {"message":"License key already added:'
                           'license with that key already exists"}'),

    # ДЛЯ СТРАНИЦЫ "РАЗРЕШЕНИЯ" РАЗДЕЛА "НАСТРОЙКИ"
    "permissions_create": "разрешение успешно создано",
    "permissions_modify": "разрешение успешно изменено",
    "permissions_delete": "разрешение успешно удалено",

    # ДЛЯ СТРАНИЦЫ "ГРУППЫ ДОСТУПА" РАЗДЕЛА "НАСТРОЙКИ"
    "access_groups_create": "группа доступа успешно создана",
    "access_groups_modify": "группа доступа успешно изменена",
    "access_groups_delete": "группа доступа успешно удалена",
    "access_groups_add": "сущность успешно добавлена",
    "access_groups_delete_user": "пользователь успешно удалён",
    "access_groups_delete_group": "группа успешно удалена",

    # ДЛЯ СТРАНИЦЫ ПОЛЬЗОВАТЕЛЯ
    "user_preparing": "Идёт подготовка сервиса, пожалуйста, подождите",
    "user_connect_success": "Сервис подготовлен к запуску",
    "user_connect_failed": "Ошибка при попытке запуска сервиса",
}
