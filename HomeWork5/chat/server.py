import socket
import sys
import os

from utils import port_check, addres, get_message, send_message
from variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, MAX_CONN

sys.path.append(os.path.join(os.getcwd(), '..'))
from log.server_log_config import log


def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    try:
        addr = addres(sys.argv)
        log.info(f'Адрес {addr} присвоен успешно')
    except ValueError as e:
        return log.error(e)
    try:
        port = port_check(sys.argv)
        log.info(f'Порт {port} присвоен успешно')
    except ValueError as err:
        return log.error(err)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((addr, port))
    server.listen(MAX_CONN)
    log.info('Сервер готов к работе')

    while True:
        client, client_addr = server.accept()
        try:
            res = get_message(client)
            log.info('Сообщение получено')
            log.info(res)
            answer = process_client_message(res)
            log.info('Ответ успешно сформирован')
            log.info(answer)
            send_message(client, answer)
            log.info('Ответ отправлен')
            client.close()
            log.info('Соединение с клиентом закрыто')
        except ValueError:
            log.error('Что то пошло не так')
            client.close()


if __name__ == '__main__':
    main()
