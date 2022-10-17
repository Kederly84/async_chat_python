# Генератор и итератор на классах:
class Generator:

    def __init__(self, start: int, stop: int):
        self.curr = start - 1
        self.stop = stop

    def __next__(self):
        if self.curr == self.stop:
            raise StopIteration
        self.curr += 1
        return self.curr


class Iterator:
    def __init__(self, obj: Generator):
        self.obj = obj

    def __iter__(self):
        return self.obj


A = Generator(1, 5)
B = Iterator(A)

for i in B:
    print(i)


# Генератор и итератор на функциях:
def generator(num: int):
    for i in range(num):
        yield i


def iterator(obj):
    while True:
        try:
            print(next(obj))
        except Exception as err:
            print(f'Exception: {type(err).__name__}')
            break


example = generator(3)
iterator(example)

# Генератор на встроенной функции range:
A = range(1, 3)
B = iter(A)
iterator(B)


# Игра fizzbuzz с запоминанием числа до которого идет игра через присоединение состояния функции
# и использования замыкания:
def wrap(num: int):
    def fizzbuzz(fizz: int, buzz: int):
        for i in range(1, fizzbuzz.state + 1):
            if i % (fizz * buzz) == 0:
                yield 'fizzbuzz'
            if i % fizz == 0:
                yield 'fizz'
            elif i % buzz == 0:
                yield 'buzz'
            else:
                yield i

    fizzbuzz.state = num
    return fizzbuzz


func = wrap(100)

for _ in func(3, 5):
    print(_)
