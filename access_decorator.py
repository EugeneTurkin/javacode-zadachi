# Создайте декоратор access_control, который ограничивает доступ к функции на основе переданных ролей пользователя.
# Декоратор должен принимать аргументы, определяющие допустимые роли (например, @access_control(roles=['admin', 'moderator'])). Требования:

# Если текущий пользователь имеет одну из допустимых ролей, функция выполняется.
# Если нет, выбрасывается исключение PermissionError с соответствующим сообщением.
# Реализуйте механизм определения текущей роли пользователя. Для целей задания можно использовать глобальную переменную или контекстный менеджер.


def access_control(roles):
    def access_decorator(func):
        def access_wrapper(*args, **kwargs):
            if "x" or "y" in roles:
                return func(*args, **kwargs)
            else:
                raise Exception
        return access_wrapper
    return access_decorator
