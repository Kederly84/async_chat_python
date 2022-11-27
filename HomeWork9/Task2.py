from ipaddress import ip_address

from Task1 import host_ping


def host_range_ping(start_ip: str, end_ip: str):
    start = ip_address(start_ip)
    end = ip_address(end_ip)
    if start_ip[:start_ip.rfind('.')] != end_ip[:start_ip.rfind('.')]:
        print('Адреса не из одной подсети')
        return
    if end <= start:
        print('Второй адрес должен быть больще первого')
        return
    diff = int(end_ip.split('.')[3]) - int(start_ip.split('.')[3])
    ip_list = map(str, [start + i for i in range(diff)])
    return host_ping(ip_list)


if __name__ == '__main__':
    print(host_range_ping('127.0.0.1', '127.0.0.10'))
