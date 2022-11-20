import socket
import sys
import select
import time

from chat_utils.utils import port_check, addres, get_message, send_message
from chat_utils.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, MAX_CONN, MESSAGE_TEXT, \
    MESSAGE, SENDER
from log.server_log_config import server_log


def process_client_message(message, messages_list, client):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return send_message(client, {RESPONSE: 200})
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    return send_message(client, {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    })


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
    server.settimeout(0.5)
    clients = []
    messages = []
    server.listen(MAX_CONN)
    server_log.info('Сервер готов к работе')

    while True:
        try:
            client, client_addr = server.accept()
        except OSError:
            pass
        else:
            clients.append(client)
        rec = []
        send = []
        err = []
        try:
            if clients:
                rec, send, err = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if rec:
            for r in rec:
                try:
                    process_client_message(get_message(r), messages, r)
                except:
                    clients.remove(r)
        if messages and send:
            print(messages)
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for s in send:
                try:
                    send_message(s, message)
                except:
                    clients.remove(s)


if __name__ == '__main__':
    main()
