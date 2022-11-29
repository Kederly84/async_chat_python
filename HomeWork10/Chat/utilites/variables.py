# Настройки по умолчанию для подключения
DEFAULT_PORT = 7777
DEFAULT_IP = '127.0.0.1'
MAX_CONN = 5
# Настройки сообщений
MAX_PACK_LEN = 1024
ENCODING = 'utf-8'

# Ключи сообщения
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'

# Параметры сообщения
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'

# Коды ответов
RESPONSE_200 = {RESPONSE: 200}
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}
