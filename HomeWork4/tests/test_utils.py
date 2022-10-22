import sys
import os
import unittest
import json

sys.path.append(os.path.join(os.getcwd(), '..'))
from utils import port_check, addres, get_message, send_message
from variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, ENCODING, MAX_SIZE, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR


class TestSocket:

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.received_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestUtils(unittest.TestCase):
    test_message = {
        ACTION: PRESENCE,
        TIME: 1,
        USER: {
            ACCOUNT_NAME: 'Guest'
        }
    }
    test_dict_recv_ok = {RESPONSE: 200}
    test_dict_recv_err = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_port_check_ok(self):
        self.assertEqual(port_check(['-p', '5432']), 5432)

    def test_default_port(self):
        self.assertEqual(port_check([]), DEFAULT_PORT)


    def test_port_err_arg(self):
        self.assertRaises(ValueError, port_check, 'После -p укажите номер порта или удалите аргумент')

    def test_adress_ok(self):
        self.assertEqual(addres(['-a', '0.0.0.0']), '0.0.0.0')


    def test_send_message(self):
        socket = TestSocket(self.test_message)
        send_message(socket, self.test_message)
        self.assertEqual(socket.encoded_message, socket.received_message)
        with self.assertRaises(Exception):
            send_message(socket, socket)

    def test_get_massage(self):
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        test_sock_err = TestSocket(self.test_dict_recv_err)
        self.assertEqual(get_message(test_sock_ok), self.test_dict_recv_ok)
        self.assertEqual(get_message(test_sock_err), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
