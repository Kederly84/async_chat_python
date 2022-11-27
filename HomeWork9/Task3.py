from Task2 import host_range_ping

from tabulate import tabulate


def host_range_ping_tab():
    res = host_range_ping('127.0.0.1', '127.0.0.10')
    result = []
    for key, val in res.items():
        result.append((key, val))
    print(tabulate(result, headers=('ip', 'Доступность')))


if __name__ == "__main__":
    host_range_ping_tab()
