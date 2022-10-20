import sys
import socket
import time
from variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE
from utils import port_check, addres, get_message, send_message


def create_presence(name: str = 'Guest'):
    message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: name
        }
    }
    return message


def main():

    addr = addres(sys.argv)
    port = port_check(sys.argv)

    messenger = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    messenger.connect((addr, port))
    send_message(messenger, create_presence())
    try:
        answer = get_message(messenger)
        if RESPONSE in answer:
            if answer[RESPONSE] == 200:
                print('200 : OK')
            if answer[RESPONSE] == 400:
                print('400 : BAD REQUEST')
    except ValueError:
        print('Не удалось прочитать сообщение сервера')


if __name__ == '__main__':
    main()


