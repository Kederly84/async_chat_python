import json
from variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, ENCODING, MAX_SIZE


def port_check(arguments: list) -> int:
    if '-p' in arguments:
        try:
            port = arguments[arguments.index('-p') + 1]
            if port.isdigit() and 1024 <= int(port) <= 65535:
                port = int(port)
            else:
                raise ValueError(f'Порт {port} указан некорректно')
        except IndexError:
            raise ValueError('После -p укажите номер порта или удалите аргумент')
    else:
        port = DEFAULT_PORT
    return port


def addres(arguments: list) -> str:
    if '-a' in arguments:
        try:
            addr = arguments[arguments.index('-a') + 1]
        except IndexError:
            raise ValueError('укажите IP адрес или удалите аргумент "-a"')
    else:
        addr = DEFAULT_IP_ADDRESS
    return addr


def get_message(client):
    encoded_response = client.recv(MAX_SIZE)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(sock, message):
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
