from contextlib import contextmanager
from functools import wraps
from os import environ


@contextmanager
def manage_roles(role):
    environ["role"] = role
    try:
        yield environ["role"]
    finally:
        del environ["role"]


class PermissionError(Exception):
    ...


def access_control(roles):
    def access_decorator(func):
        @wraps(func)
        def access_wrapper(*args, **kwargs):
            if environ["role"] in roles:
                    return func(*args, **kwargs)
            raise PermissionError("Access denied")
        return access_wrapper
    return access_decorator


@access_control(roles=["admin", "moderator"])
def admin_func(*args):
    return str(args)


with manage_roles("admin") as admin_role:
    admin_func("foo")

with manage_roles("student") as student_role:
    admin_func("foo")
