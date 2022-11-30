import logging.handlers
import os.path

LOG_SERVER = logging.getLogger('server')

file_path = os.path.join(os.path.abspath(__file__), '..', "server.log")
FILE_HANDLER = logging.handlers.TimedRotatingFileHandler(file_path, encoding='utf-8', when='d')
FILE_HANDLER.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter("%(asctime)s %(levelname)s %(module)s %(message)s ")

FILE_HANDLER.setFormatter(FORMATTER)

LOG_SERVER.addHandler(FILE_HANDLER)
LOG_SERVER.setLevel(logging.DEBUG)

if __name__ == '__main__':
    LOG_SERVER.info('Лог сервера вроде работает')
