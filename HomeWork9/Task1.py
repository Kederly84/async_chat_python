import platform
from subprocess import Popen, PIPE
from threading import Thread


def ping(ip, res: list):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, '1', ip]
    reply = Popen(args, stdout=PIPE, stderr=PIPE)

    code = reply.wait()
    if code == 0:
        res.append('Узел доступен')
    else:
        res.append('Узел недоступен')
    return


def host_ping(list_ip):
    list_treads = {}
    for ip in list_ip:
        res = []
        thread = Thread(target=ping, args=(ip, res))
        list_treads[ip] = (thread, res)
        thread.start()
    results = {}
    for ip, (t, res) in list_treads.items():
        t.join()
        results[ip] = res[0]

    return results


if __name__ == '__main__':
    ip_addresses = ['yandex.ru', '2.2.2.2', 'google.com', '127.0.0.1']
    print(host_ping(ip_addresses))
