import os
import socket
import sys
import time

from utils import port_check, addres, get_message, send_message
from variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE

sys.path.append(os.path.join(os.getcwd(), '..'))
from log.client_log_config import client_log


def create_presence(name: str = 'Guest'):
    message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: name
        }
    }
    client_log.info(f'Сообщение {message} сформировано')
    return message


def answer(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        if message[RESPONSE] == 400:
            return '400 : BAD REQUEST'
    else:
        raise ValueError


def main():
    try:
        addr = addres(sys.argv)
    except ValueError as e:
        return client_log.error(e)
    try:
        port = port_check(sys.argv)
    except ValueError as err:
        return client_log.error(err)

    messenger = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    messenger.connect((addr, port))
    client_log.info('Соединение с сервером установлено')
    client_log.info(send_message(messenger, create_presence()))
    client_log.info('Запрос отправлен')
    try:
        ans = get_message(messenger)
        client_log.info('Ответ получен')
        mes = answer(ans)
        client_log.info(f'Ответ {mes} успешно обработан')
    except ValueError:
        client_log.error('Не удалось прочитать сообщение сервера')


if __name__ == '__main__':
    main()
