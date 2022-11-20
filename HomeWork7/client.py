import socket
import sys
import time

from chat_utils.utils import port_check, addres, get_message, send_message, client_mode
from chat_utils.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, MESSAGE, SENDER, MESSAGE_TEXT
from log.client_log_config import client_log


def get_mesage_from_server(message):
    if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя {message[SENDER]} с текстом: {message[MESSAGE_TEXT]}')


def create_message(sock, name: str = 'Guest'):
    message = input('Введите сообщение для отправки или наберите "Exit" для выхода: ')
    if message == 'Exit':
        sock.close()
        sys.exit()
    message_to_send = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: name,
        MESSAGE_TEXT: message
    }
    return message_to_send


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
        port = port_check(sys.argv)
        mode = client_mode(sys.argv)
    except ValueError as err:
        client_log.error(err)
        sys.exit(1)
    try:
        messenger = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        messenger.connect((addr, port))
        client_log.info('Соединение с сервером установлено')
        send_message(messenger, create_presence())
        client_log.info('Запрос отправлен')
        answer(get_message(messenger))
        print('Установлено соединение с сервером')
    except ValueError as e:
        client_log.error(e)
    else:
        if mode == 'send':
            try:
                mess = create_message(messenger)
                send_message(messenger, mess)
            except:
                client_log.error('Соединение с сервером было потеряно')
                sys.exit(1)
        if mode == 'listen':
            try:
                get_mesage_from_server(get_message(messenger))
            except:
                client_log.error('Соединение с сервером было потеряно')


if __name__ == '__main__':
    main()
