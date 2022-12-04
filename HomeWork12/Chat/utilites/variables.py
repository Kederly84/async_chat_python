# Настройки по умолчанию для подключения
DEFAULT_PORT = 7777
DEFAULT_IP = '127.0.0.1'
MAX_CONN = 5
# Настройки сообщений
MAX_PACK_LEN = 1024
ENCODING = 'utf-8'

# Ключи сообщения
ACTION = 'action'
ALERT = 'alert'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'
ADD_CONTACT = 'add_contact'
USER_ID = 'user_id'
DEL_CONTACT = 'del_contact'

# Параметры сообщения
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'
GET_CONTACTS = 'get_contacts'

# Коды ответов
RESPONSE_200 = {RESPONSE: 200}
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}
RESPONSE_202 = {
    RESPONSE: 202,
    ALERT: None
}

CONTACTS = {
    ACTION: None,
    TIME: None,
    ACCOUNT_NAME: None,
    USER_ID: None
}
