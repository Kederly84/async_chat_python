import logging
import os.path

LOG_CLIENT = logging.getLogger('client')

file_path = os.path.join(os.path.abspath(__file__), '..', "client.log")
FILE_HANDLER = logging.FileHandler(file_path, encoding='utf-8')
FILE_HANDLER.setLevel(logging.DEBUG)
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(logging.INFO)

FORMATTER = logging.Formatter("%(asctime)s %(levelname)s %(module)s %(message)s ")

FILE_HANDLER.setFormatter(FORMATTER)
STREAM_HANDLER.setFormatter(FORMATTER)


LOG_CLIENT.addHandler(FILE_HANDLER)
LOG_CLIENT.addHandler(STREAM_HANDLER)
LOG_CLIENT.setLevel(logging.DEBUG)

if __name__ == '__main__':
    LOG_CLIENT.info('Лог клиента вроде работает')
