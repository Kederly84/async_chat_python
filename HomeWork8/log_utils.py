import inspect
import sys
import traceback
from functools import wraps

from log.client_log_config import client_log
from log.server_log_config import server_log


def log(func):
    @wraps(func)
    def inner(*args, **kwargs):
        client = False
        server = True
        if 'client.py' in sys.argv[0]:
            client = True
            server = False
        arg = ', '.join(list(map(str, args)) + [f'{key}={val}' for key, val in kwargs.items()])
        msg = f'функция {func.__name__}({arg}) Вызов из модуля {func.__module__}. Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}. Вызов из функции {inspect.stack()[1][3]}'
        write_log(client, server, msg)
        return func(*args, **kwargs)

    return inner


def write_log(client: bool, server: bool, message: str) -> None:
    if client:
        client_log.info(message)
    if server:
        server_log.info(message)
