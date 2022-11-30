from utilites.errors import IncorrectPort


class PortDescr:

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if isinstance(value, str) and value.isdigit():
            value = int(value)
        if isinstance(value, int) and 1024 <= value <= 65535:
            instance.__dict__[self.name] = value
            return
        raise IncorrectPort('')

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]
