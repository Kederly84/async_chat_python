class IncorrectDataRecivedError(Exception):

    def __str__(self):
        return 'Принято некорректное сообщение от клиента'


class NoDictInputError(Exception):

    def __str__(self):
        return 'Аргумент должен быть словарём.'


class IncorrectPort(Exception):

    def __str__(self):
        return 'указан некорректный порт'


class ServerError(Exception):

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class ReqFieldMissingError(Exception):

    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'В принятом словаре отсутствует обязательное поле {self.missing_field}.'
