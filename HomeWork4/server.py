import socket
import sys
from variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, MAX_CONN
from utils import port_check, addres, get_message, send_message


def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():

    addr = addres(sys.argv)
    port = port_check(sys.argv)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((addr, port))
    server.listen(MAX_CONN)

    while True:
        client, client_addr = server.accept()
        try:
            res = get_message(client)
            print(res)
            answer = process_client_message(res)
            print(answer)
            send_message(client, answer)
            client.close()
        except ValueError:
            print('Что то пошло не так')
            client.close()


if __name__ == '__main__':
    main()
