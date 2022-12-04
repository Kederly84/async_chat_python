import sys
from functools import wraps
from log.server_log_config import LOG_SERVER
from log.client_log_config import LOG_CLIENT

if sys.argv[0].find('server') == -1:
    loger = LOG_CLIENT
else:
    loger = LOG_SERVER


def log(func):
    @wraps(func)
    def saver(*args, **kwargs):
        loger.debug(
            f'Была вызвана функция {func.__name__} c параметрами {args} , {kwargs}. Вызов из модуля {func.__module__}')
        return func(*args, **kwargs)
    return saver
