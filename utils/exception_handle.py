class ExceptionHandler:
    """Класс для обработки исключений"""
    def handle_exception(self, func):
        """Декоратор для обработки исключений"""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Ошибка в функции {func.__name__}: {e}")
                raise
        return wrapper
