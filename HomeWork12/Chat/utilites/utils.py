import json
import sys

sys.path.append('../')
from log_decor import log
from utilites import variables, errors


@log
def get_mess(client):
    encoded_response = client.recv(variables.MAX_PACK_LEN)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(variables.ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        else:
            raise errors.IncorrectDataRecivedError
    else:
        raise errors.IncorrectDataRecivedError


@log
def send_mess(sock, message):
    if not isinstance(message, dict):
        raise errors.NoDictInputError
    json_message = json.dumps(message)
    enc_mess = json_message.encode(variables.ENCODING)
    sock.send(enc_mess)
