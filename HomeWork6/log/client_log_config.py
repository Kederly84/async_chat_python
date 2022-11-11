import logging
import os.path

client_log = logging.getLogger('client')

file_path = os.path.join(os.path.abspath(__file__), '..', "client.log")
FILE_HANDLER = logging.FileHandler(file_path, encoding='utf-8')
FILE_HANDLER.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter("%(asctime)s %(levelname)s %(module)s %(message)s ")

FILE_HANDLER.setFormatter(FORMATTER)

client_log.addHandler(FILE_HANDLER)
client_log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    client_log.info('check')
