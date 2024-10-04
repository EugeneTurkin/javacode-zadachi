from collections import OrderedDict
from functools import wraps


def cache(_func=None, *, max_size=3):
    cache = OrderedDict().get

    def caching_decorator(func):
        """
        Кешируем результаты вызовов функций на основе её аргументов.
        При индентичном повторном вызове возвращаем результат из кеша вместо повторного выполнения функции.
        """
        @wraps(func)
        def wrapper(*args):
            if args in cache:  # если вызов уже в кеше, возвращаем кешированное значение
                return cache[args]
            if len(cache) == max_size:  # размер кеша снижен для простоты проверки
                cache.popitem(last=False)  # удаление старых записей в стиле FIFO
            cache[args] = func(*args)

            return cache[args]
        return wrapper

    if _func is None:
        return caching_decorator
    else:
        return caching_decorator(_func)


@cache(max_size=3)
def funct(*args):
    return len(args)


# Моковые вызовы для проверки через дебаггер.
funct(1, "foo")
funct(1, "foo")
funct(2, "bar")
funct(3, "baz")
funct(4, "foobar")
