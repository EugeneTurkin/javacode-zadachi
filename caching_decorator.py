from collections import OrderedDict
import functools


def caching_decorator(
        func,
        _cache = OrderedDict(),  # упорядоченный словарь позволит управлять порядком удаления записей
    ):
    """
    Кешируем результаты вызовов функций на основе её аргументов.
    При индентичном повторном вызове возвращаем результат из кеша вместо повторного выполнения функции.
    """
    @functools.wraps(func)
    def wrapper(*args):
        if args in _cache.keys():  # если вызов уже в кеше, возвращаем кешированное значение
            return _cache[args]
        if len(_cache) == 3:  # размер кеша снижен для простоты проверки
            _cache.popitem(last=False)  # удаление старых записей в стиле FIFO
        _cache[args] = func(*args)

        return _cache[args]
    return wrapper


@caching_decorator
def funct(*args):
    return len(args)


# Моковые вызовы для проверки через дебаггер.
funct(1, "foo")
funct(1, "foo")
funct(2, "bar")
funct(3, "baz")
funct(4, "foobar")


# TODO: так как кеш - это словарь, а аргументы функции - его ключи, они должны быть хешируемыми. для этого в декортатор
# можно добавить try.. except на случай, если в функцию попытаются передать не hashable аргумент
# TODO: также можно в декораторе парсить кварги и добавлять их в ключ, написать тесты, но не уверен насколько нужно
# углубляться в контексте одной задачи
