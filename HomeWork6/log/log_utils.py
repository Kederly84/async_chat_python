import inspect
import sys
from functools import wraps

from . import client_log_config
from . import server_log_config


def log(func):

    @wraps(func)
    def inner(*args, **kwargs):
        client = False
        server = True
        if 'client.py' in sys.argv[0]:
            client = True
            server = False
        arg = ', '.join(list(map(str, args)) + [f'{key}={val}' for key, val in kwargs.items()])
        msg = f'функция {func.__name__}({arg}) вызвана из функции {inspect.stack()[1].function} '
        write_log(client, server, msg)
        return func(*args, **kwargs)

    return inner


def write_log(client: bool, server: bool, message: str) -> None:
    if client:
        client_log_config.client_log.info(message)
    if server:
        server_log_config.server_log.info(message)
