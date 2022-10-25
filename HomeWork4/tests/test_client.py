import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from client import create_presence, answer
from variables import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE

class TestClient(unittest.TestCase):

    def test_create_presence(self):
        test_message = create_presence()
        test_message[TIME] = 1
        self.assertEqual(test_message, {ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_first_ans(self):
        self.assertEqual(answer({RESPONSE: 200}), '200 : OK')

    def test_second_ans(self):
        self.assertEqual(answer({RESPONSE: 400}), '400 : BAD REQUEST')

    def test_third_ans(self):
        self.assertRaises(ValueError, answer, 'Не удалось прочитать сообщение сервера')


if __name__ == '__main__':
    unittest.main()
