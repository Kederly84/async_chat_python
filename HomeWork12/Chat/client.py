import argparse
import json
import socket
import sys
import time
from threading import Thread
from datetime import datetime

from log.client_log_config import LOG_CLIENT
from log_decor import log
from meta import ClientVerifier
from utilites.errors import IncorrectDataRecivedError, ServerError, ReqFieldMissingError
from utilites.utils import send_mess, get_mess
from utilites.variables import ACTION, ERROR, EXIT, TIME, ACCOUNT_NAME, MESSAGE, SENDER, DESTINATION, MESSAGE_TEXT, \
    PRESENCE, RESPONSE, DEFAULT_IP, DEFAULT_PORT, USER, GET_CONTACTS, ALERT, CONTACTS, DEL_CONTACT, ADD_CONTACT, USER_ID
from client_db import ClientDB

logger = LOG_CLIENT


# Класс формировки и отправки сообщений на сервер и взаимодействия с пользователем.
class ClientSender(Thread, metaclass=ClientVerifier):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        self.db = ClientDB(account_name)
        super().__init__()

    # Функция создаёт словарь с сообщением о выходе.
    def create_exit_message(self):
        return {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.account_name
        }

    def get_contacts(self):
        message_dict = {
            ACTION: GET_CONTACTS,
            ACCOUNT_NAME: self.account_name,
            TIME: time.time(),
        }
        send_mess(self.sock, message_dict)

    def add_contact(self):
        message_dict = CONTACTS
        message_dict[ACTION] = ADD_CONTACT
        message_dict[TIME] = time.time()
        message_dict[ACCOUNT_NAME] = self.account_name
        message_dict[USER_ID] = input('Введите имя пользователя, кого хотите добавить в контакты: ')
        send_mess(self.sock, message_dict)
        self.db.add_contact(message_dict[USER_ID])

    def del_contact(self):
        message_dict = CONTACTS
        message_dict[ACTION] = DEL_CONTACT
        message_dict[TIME] = time.time()
        message_dict[ACCOUNT_NAME] = self.account_name
        message_dict[USER_ID] = input('Введите имя пользователя, кого хотите удалить из контактов: ')
        send_mess(self.sock, message_dict)
        self.db.del_contact(message_dict[USER_ID])

    # Функция запрашивает кому отправить сообщение и само сообщение, и отправляет полученные данные на сервер.
    def create_message(self):
        to = input('Введите получателя сообщения: ')
        message = input('Введите сообщение для отправки: ')
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.account_name,
            DESTINATION: to,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        logger.debug(f'Сформирован словарь сообщения: {message_dict}')
        try:
            send_mess(self.sock, message_dict)
            logger.info(f'Отправлено сообщение для пользователя {to}')
            self.db.add_message(message_dict[SENDER], message_dict[DESTINATION], message_dict[MESSAGE_TEXT],
                                datetime.fromtimestamp(message_dict[TIME]))
        except:
            logger.critical('Потеряно соединение с сервером.')
            exit(1)

    def run(self):
        self.print_help()
        while True:
            command = input('Введите команду: ')
            if command == 'message':
                self.create_message()
            elif command == 'help':
                self.print_help()
            elif command == 'exit':
                try:
                    send_mess(self.sock, self.create_exit_message())
                except:
                    pass
                print('Завершение соединения.')
                logger.info('Завершение работы по команде пользователя.')
                # Задержка неоходима, чтобы успело уйти сообщение о выходе
                time.sleep(0.5)
                break
            elif command == 'contacts':
                self.get_contacts()
            elif command == 'add':
                self.add_contact()
            elif command == 'del':
                self.del_contact()
            else:
                print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')

    @staticmethod
    def print_help():
        print('Поддерживаемые команды:')
        print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
        print('help - вывести подсказки по командам')
        print('exit - выход из программы')
        print('contacts - получить список контактов')
        print('add - Добавить пользователя в список контактов')
        print('del - удалить пользователя из списка контактов')


class ClientReader(Thread, metaclass=ClientVerifier):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()

    def run(self):
        while True:
            try:
                message = get_mess(self.sock)
                if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and DESTINATION in message \
                        and MESSAGE_TEXT in message and message[DESTINATION] == self.account_name:
                    print(f'\nПолучено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
                    logger.info(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
                elif RESPONSE in message and message[RESPONSE] == 202:
                    print(f'Список контактов: {message[ALERT]}')
                elif RESPONSE in message and message[RESPONSE] == 200:
                    print(f'Операция выполнена успешно')
                else:
                    logger.error(f'Получено некорректное сообщение с сервера: {message}')
            except IncorrectDataRecivedError:
                logger.error(f'Не удалось декодировать полученное сообщение.')
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
                logger.critical(f'Потеряно соединение с сервером.')
                break


@log
def create_presence(account_name):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


@log
def process_response_ans(message):
    logger.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default=DEFAULT_IP, nargs='?')
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.a
    server_port = namespace.p
    client_name = namespace.n

    if not 1023 < server_port < 65536:
        logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        exit(1)

    return server_address, server_port, client_name


def main():
    print('Консольный месседжер. Клиентский модуль.')
    server_address, server_port, client_name = arg_parser()
    if not client_name:
        client_name = input('Введите имя пользователя: ')
    else:
        print(f'Клиентский модуль запущен с именем: {client_name}')

    logger.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address} , порт: {server_port}, '
        f'имя пользователя: {client_name}')
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_mess(transport, create_presence(client_name))
        answer = process_response_ans(get_mess(transport))
        logger.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        logger.error('Не удалось декодировать полученную Json строку.')
        exit(1)
    except ServerError as error:
        logger.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        exit(1)
    except ReqFieldMissingError as missing_error:
        logger.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        exit(1)
    except (ConnectionRefusedError, ConnectionError):
        logger.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        exit(1)
    else:
        module_reciver = ClientReader(client_name, transport)
        module_reciver.daemon = True
        module_reciver.start()
        module_sender = ClientSender(client_name, transport)
        module_sender.daemon = True
        module_sender.start()
        logger.debug('Запущены процессы')

        while True:
            time.sleep(1)
            if module_reciver.is_alive() and module_sender.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
