import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from server import process_client_message
from variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, MAX_CONN


class TestServer(unittest.TestCase):
    corr_ans = {RESPONSE: 200}
    uncorr_ans = {RESPONSE: 400, ERROR: 'Bad Request'}
    corr_presence = {
        ACTION: PRESENCE,
        TIME: 1,
        USER: {
            ACCOUNT_NAME: 'Guest'
        }
    }

    def test_no_action(self):
        test_dict = {
            TIME: 1,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }
        self.assertEqual(process_client_message(test_dict), self.uncorr_ans)

    def test_no_time(self):
        test_dict = {
            ACTION: PRESENCE,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }
        self.assertEqual(process_client_message(test_dict), self.uncorr_ans)

    def test_no_user(self):
        test_dict = {
            ACTION: PRESENCE,
            TIME: 1,
        }
        self.assertEqual(process_client_message(test_dict), self.uncorr_ans)

    def test_wrong_user(self):
        test_mess = {
            ACTION: PRESENCE,
            TIME: 1,
            USER: {
                ACCOUNT_NAME: 'Путин'
            }
        }
        self.assertEqual(process_client_message(test_mess), self.uncorr_ans)

    def test_all_ok(self):
        self.assertEqual(process_client_message(self.corr_presence), self.corr_ans)


if __name__ == '__main__':
    unittest.main()
