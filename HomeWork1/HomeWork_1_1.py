import subprocess
import locale
import chardet

# Задание 1
print("\nЗадание 1")
words = ["разработка", "сокет", "декоратор"]
for word in words:
    print(type(word), word)
# Преобразовано с помощью https://www.branah.com/unicode-converter в кодировку UTF-16
words_unicode = {
    "разработка": "\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430",
    "сокет": "\u0441\u043e\u043a\u0435\u0442",
    "декоратор": "\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440"
}
for value in words_unicode.values():
    print(type(value), value)

# Задание 2
print("\nЗадание 2")
class_bytes = b"class"
function_bytes = b"function"
method_bytes = b"method"
words_arr = [class_bytes, function_bytes, method_bytes]
for elem in words_arr:
    print(type(elem), len(elem), elem)

# Задание 3
print("\nЗадание 3")
examples = ['attribute', 'класс', 'функция', 'type']
for example in examples:
    try:
        ex = example.encode('ascii')
        print(type(ex), len(ex), ex)
    except UnicodeError as err:
        print(f'UnicodeError: {err}')

# Задание 4
print("\nЗадание 4")
examples_words = ['разработка', 'администрирование', 'protocol', 'standard']
for example_word in examples_words:
    print(example_word.encode('utf8'), example_word.encode('utf8').decode('utf8'))

# Задание 5
print("\nЗадание 5")
for site in ['yandex.ru', 'youtube.com']:
    args = ['ping', site]
    with subprocess.Popen(args, stdout=subprocess.PIPE) as subprocess_ping:
        for index, line in enumerate(subprocess_ping.stdout):
            res = chardet.detect(line)
            print(line.decode(res['encoding']), end='')
            if index >= 5:
                break

# Задание 6
print("\nЗадание 6")
detector = chardet.UniversalDetector()
with open('test_file.txt', 'rb') as file:
    for _ in file:
        detector.feed(_)
        if detector.done:
            break
    detector.close()
with open('test_file.txt', encoding=detector.result['encoding']) as text_file:
    for line in text_file:
        print(line, end='')
