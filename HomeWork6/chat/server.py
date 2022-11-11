import socket
import sys
import os

from utils import port_check, addres, get_message, send_message
from variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, MAX_CONN

sys.path.append(os.path.join(os.getcwd(), '..'))
from log.server_log_config import server_log


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
        server_log.info(f'Адрес {addr} присвоен успешно')
    except ValueError as e:
        return server_log.error(e)
    try:
        port = port_check(sys.argv)
        server_log.info(f'Порт {port} присвоен успешно')
    except ValueError as err:
        return server_log.error(err)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((addr, port))
    server.listen(MAX_CONN)
    server_log.info('Сервер готов к работе')

    while True:
        client, client_addr = server.accept()
        try:
            res = get_message(client)
            server_log.info('Сообщение получено')
            server_log.info(res)
            answer = process_client_message(res)
            server_log.info('Ответ успешно сформирован')
            server_log.info(answer)
            send_message(client, answer)
            server_log.info('Ответ отправлен')
            client.close()
            server_log.info('Соединение с клиентом закрыто')
        except ValueError:
            server_log.error('Что то пошло не так')
            client.close()


if __name__ == '__main__':
    main()
